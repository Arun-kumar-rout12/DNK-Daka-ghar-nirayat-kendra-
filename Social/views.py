import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import *
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
import random
import uuid
from reportlab.pdfgen import canvas
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import person, Receipt
from django.core.files.base import ContentFile
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.user.is_authenticated:
        # Ensure user has a profile
        if not hasattr(request.user, 'userprofile'):
            UserProfile.objects.create(user=request.user)
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Ensure user has a profile
            if not hasattr(user, 'userprofile'):
                UserProfile.objects.create(user=user)
            return redirect('home')
        else:
            error = "Invalid username or password."
            return render(request, 'index.html', {'error': error})

    return render(request, 'index.html')
def Aindex(request):
    if request.method == 'POST':
        agent_name = request.POST.get('username')
        agent_id = request.POST.get('agent_id')

        try:
            # Validate the agent
            agent = AgentProfile.objects.get(name=agent_name, agent_id=agent_id)
            request.session['agent_id'] = agent.agent_id  # Store agent ID in session
            messages.success(request, "Login successful!")
            return redirect('Ahome')  # Redirect to the agent home page
        except AgentProfile.DoesNotExist:
            messages.error(request, "Invalid login credentials. Agent does not exist.")

    return render(request, 'Aindex.html')

def Ahome(request):
    agent_id = request.session.get('agent_id')

    if agent_id:
        try:
            # Fetch the agent's profile based on the stored agent_id
            agent_profile = AgentProfile.objects.get(agent_id=agent_id)
            persons = person.objects.all()  # Fetch all persons

            # Pass the agent profile and persons data to the template
            context = {
                'AgentProfile': agent_profile,
                'persons': persons,
            }
            return render(request, 'Ahome.html', context)

        except AgentProfile.DoesNotExist:
            messages.error(request, "Agent not found.")
            return redirect('Aindex') 
    else:
        messages.error(request, "Please log in first.")
        return redirect('Aindex')
    
def Aprofile(request):
    agent_id = request.session.get('agent_id')

    if agent_id:
        try:
            agent_profile = AgentProfile.objects.get(agent_id=agent_id)
            context = {
                'name': agent_profile.name,
                'agent_id': agent_profile.agent_id,
                'phone_number': agent_profile.phone_number,
            }
            return render(request, 'Aprofile.html', context)
        except AgentProfile.DoesNotExist:
            messages.error(request, "Agent not found.")
            return redirect('Aindex')
    else:
        messages.error(request, "Please log in first.")
        return redirect('Aindex')



def update_Aprofile(request):
    agent_id = request.session.get('agent_id')

    if agent_id:
        try:
            agent_profile = AgentProfile.objects.get(agent_id=agent_id)
            if request.method == 'POST':
                agent_name = request.POST.get('agent_name', agent_profile.name)
                phone_number = request.POST.get('phone_number', agent_profile.phone_number)

                # Update profile data
                agent_profile.name = agent_name
                agent_profile.phone_number = phone_number
                agent_profile.save()

                messages.success(request, "Profile updated successfully!")
                return redirect('Aprofile')

            # Render the update form with current agent details
            return render(request, 'update_Aprofile.html', {
                'agent_name': agent_profile.name,
                'phone_number': agent_profile.phone_number,
            })
        except AgentProfile.DoesNotExist:
            messages.error(request, "Agent not found.")
            return redirect('Aindex')
    else:
        messages.error(request, "Please log in first.")
        return redirect('Aindex')


@login_required(login_url='index')
def home(request):
    total_shipments = person.objects.filter(user=request.user).count()
    po_induction_pending_count = person.objects.filter(user=request.user, status='pending').count()
    in_transit_count = person.objects.filter(user=request.user, status='Transit').count()
    under_processing_count = person.objects.filter(user=request.user, status='processing').count()
    customs_cleared_count = person.objects.filter(user=request.user, status='Cleared').count()
    customs_detained_count = person.objects.filter(user=request.user, status='detained').count()
    despatched_out_of_india_count = person.objects.filter(user=request.user, status='Despatched').count()

    persons = person.objects.filter(user=request.user)

    # Generate 6 random values (e.g., between 1000 and 9999) for each of the 6 boxes
    random_box_values = {
        'box1': random.randint(1000, 9999),
        'box2': random.randint(1000, 9999),
        'box3': random.randint(1000, 9999),
        'box4': random.randint(1000, 9999),
        'box5': random.randint(1000, 9999),
        'box6': random.randint(1000, 9999),
    }

    return render(request, 'home.html', {
        'user': request.user,
        'total_shipments': total_shipments,
        'po_induction_pending_count': po_induction_pending_count,
        'in_transit_count': in_transit_count,
        'under_processing_count': under_processing_count,
        'customs_cleared_count': customs_cleared_count,
        'customs_detained_count': customs_detained_count,
        'despatched_out_of_india_count': despatched_out_of_india_count,
        'persons': persons,
        'random_box_values': random_box_values,  
    })



@login_required(login_url='index')
def profile(request):
    user_profile = request.user.userprofile
    return render(request, 'profile.html', {
        'bio': user_profile.bio,
    })


@login_required(login_url='index')
def delete_post(request, post_id):
    post = get_object_or_404(UserPost, id=post_id, user=request.user)
    post.delete()
    return redirect('home')


@login_required(login_url='index')
def update_profile(request):
    if request.method == 'POST':
        user = request.user 


        username = request.POST.get('name')
        if username and username != user.username:
            user.username = username


        password = request.POST.get('password')
        if password:
            user.set_password(password)  
            user.save()
            messages.success(request, 'Profile updated successfully. Please log in again.')  
            return redirect('index')

        user.save()  

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'update_profile.html')



@login_required(login_url='index')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content:
            UserPost.objects.create(user=request.user, post=content)
        return redirect('home')
    
    return render(request, 'create_post.html')


@login_required(login_url='index')
def signout(request):
    user_profile = request.user.userprofile
    user_profile.status = 'offline'
    user_profile.save()
    logout(request)
    return redirect('index')


def Aregistration(request):
    return render(request, 'Aregistration.html')


def generate_unique_agent_id():
    while True:
        agent_id = 'DNK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if not AgentProfile.objects.filter(agent_id=agent_id).exists():
            return agent_id

def Aregistration1(request):
    if request.method == 'POST':
        agent_name = request.POST.get('agent_name')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not agent_name or not phone_number:
            return render(request, 'Aregistration.html', {'error': 'Agent name and phone number are required.'})
        
        if password != confirm_password:
            return render(request, 'Aregistration.html', {'error': 'Passwords do not match. Please try again.'})

        try:
            agent_id = generate_unique_agent_id()

            AgentProfile.objects.create(
                name=agent_name,
                phone_number=phone_number,
                agent_id=agent_id,
                password=make_password(password)
            )

            messages.success(request, "Agent registration successful!")
            request.session['agent_id'] = agent_id
            return redirect('Ahome')

        
        except IntegrityError:
            return render(request, 'Aregistration.html', {'error': 'Agent registration failed. Please try again.'})

    return render(request, 'Aregistration.html')

def generate_unique_order_id():
    while True:
        order_id = str(uuid.uuid4())[:12] 
        if not person.objects.filter(order_id=order_id).exists():
            return order_id


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'registeration.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registeration.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('home')

    return render(request, 'registeration.html')

@login_required(login_url='index')
def add_person(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Unknown')
        contact_number = request.POST.get('contact_number', None)
        from_address = request.POST.get('from_address')
        to_address = request.POST.get('to_address')
        current_address = request.POST.get('current_address', None)
        description = request.POST.get('description')
        weight = request.POST.get('weight')
        pickup_date = request.POST.get('pickup_date')
        payment_method = request.POST.get('payment_method')
        payment_details = request.POST.get('payment_details', None)
        status = request.POST.get('status', 'pending')
        signature = request.FILES.get('signature')

        if not from_address or not to_address:
            error = "Please fill out all the required address fields."
            return render(request, 'Shipment.html', {'error': error})

        order_id = generate_unique_order_id()

        new_person = person.objects.create(
            order_id=order_id,
            user=request.user,
            name=name,
            contact_number=contact_number,
            from_address=from_address,
            to_address=to_address,
            current_address=current_address,
            description=description,
            weight=weight,
            pickup_date=pickup_date,
            payment_method=payment_method,
            payment_details=payment_details,
            status=status,
            signature=signature,
            payment_status='processing'
        )

        generate_receipt(new_person)

        return redirect('view_receipt', shipment_id=new_person.id)

    return render(request, 'Shipment.html')


def generate_receipt(shipment):
    receipt, created = Receipt.objects.get_or_create(shipment=shipment)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    p.drawString(100, 800, f"Receipt Number: {receipt.receipt_number}")
    p.drawString(100, 780, f"Order ID: {shipment.order_id}")
    p.drawString(100, 760, f"Customer Name: {shipment.name}")
    p.drawString(100, 740, f"Contact Number: {shipment.contact_number}")
    p.drawString(100, 720, f"From Address: {shipment.from_address}")
    p.drawString(100, 700, f"To Address: {shipment.to_address}")
    p.drawString(100, 680, f"Current Address: {shipment.current_address}")
    p.drawString(100, 660, f"Weight: {shipment.weight} kg")
    p.drawString(100, 640, f"Pickup Date: {shipment.pickup_date.strftime('%Y-%m-%d')}")
    p.drawString(100, 620, f"Payment Method: {shipment.payment_method}")
    p.drawString(100, 600, f"Amount Paid: {receipt.amount}")
    p.drawString(100, 580, f"Status: {shipment.status}")
    
    p.showPage()
    p.save()
    buffer.seek(0)
    
    pdf_name = f"Receipt_{receipt.receipt_number}.pdf"
    receipt.pdf_file.save(pdf_name, ContentFile(buffer.read()), save=True)
    buffer.close()


@login_required(login_url='index')
def view_receipt(request, shipment_id):
    shipment = get_object_or_404(person, id=shipment_id)
    receipt = get_object_or_404(Receipt, shipment=shipment)

    return render(request, 'view_receipt.html', {
        'receipt': receipt,
    })
    
def Track(request, order_id):
    try:
        order = person.objects.get(order_id=order_id)

        if request.method == 'POST':
            agent_id = request.POST.get('agent_id')
            current_location = request.POST.get('current_location')

            try:
                agent = AgentProfile.objects.get(agent_id=agent_id)
                order.current_location = current_location
                order.save()

                messages.success(request, "Order status updated successfully!")
                return redirect('Track', order_id=order_id)

            except AgentProfile.DoesNotExist:
                messages.error(request, "Invalid agent ID. Please try again.")
                return redirect('Track', order_id=order_id)

        context = {
            'order_id': order.order_id,
            'name': order.name,
            'from_address': order.from_address,
            'to_address': order.to_address,
            'status': order.status,
            'current_location': order.current_location,
        }

        return render(request, 'Track.html', context)

    except person.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('Ahome') 
@login_required(login_url='index')    
def ViewShipmentDetails(request, order_id):
    try:
        order = person.objects.get(order_id=order_id)
        context = {
            'order_id': order.order_id,
            'name': order.name,
            'from_address': order.from_address,
            'to_address': order.to_address,
            'status': order.status,
            'current_location': order.current_location, 
        }

        return render(request, 'Track1.html', context)

    except person.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('home') 


