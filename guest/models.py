from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.humanize.templatetags import humanize



# User profile model
class ProfilePic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='avatar.jpg', upload_to='userProfilePicture')

    def __str__(self):
        return f'{self.user.username} - Profile'

    def save(self, *args, **kwargs):
        super(ProfilePic, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



# Contact Model
class ContactModel(models.Model):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    subject = models.CharField(max_length=200)
    query = models.CharField(max_length=700)
    date = models.DateTimeField(auto_now_add=True)

    def subject_snipet(self):
        return self.subject[:20] + '...'
    def query_snipet(self):
        return self.query[:30] + '...'



# Add New room Model 
class AddroomModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=4, verbose_name='title')
    name = models.CharField(max_length=100, verbose_name='name')
    email = models.CharField(max_length=100, verbose_name='email')
    contact = models.CharField(max_length=100, verbose_name='conatact', blank=True, null=True)
    for_rent = models.CharField(max_length=20)
    water_supply = models.CharField(max_length=20)
    kitchen = models.CharField(max_length=20, blank=True, null=True)
    washroom = models.CharField(max_length=20)
    parking_space = models.CharField(max_length=20, blank=True, null=True)
    troom = models.PositiveIntegerField()
    ### 'max_length' is ignored when used with PositiveIntegerField.HINT: Remove 'max_length' from field  ###
    address = models.CharField(max_length=200)
    nearest_city = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField()  
    desc = models.CharField(max_length=1000, default='')
    rmg1 = models.ImageField(default='image1.jpg', upload_to="roomImages")
    rmg2 = models.ImageField(default='image2.jpg', upload_to="roomImages")
    rmg3 = models.ImageField(default='image3.png', upload_to="roomImages")
    agreement = models.FileField(default='default_agreement.pdf', upload_to="roomAgreement")
    pub_date = models.DateTimeField(auto_now_add=True)

    def get_pub_date(self):
        return humanize.naturaltime(self.pub_date)

    def save(self, *args, **kwargs):
        self.nearest_city = self.nearest_city.upper()
        self.district = self.district.upper()
        self.address = self.address.upper()
        return super(AddroomModel, self).save(*args, **kwargs)



# Guest Reviews model
exp = [('Below Average', 'Below Average'), ('Average', 'Average'), ('Good', 'Good'), ('Better', 'Better'), ('Excellent', 'Excellent')]
class GuestReviewsModel(models.Model):
    addroommodel = models.ForeignKey(AddroomModel, on_delete=models.CASCADE)
    experience = models.CharField(choices=exp, max_length=50)
    name = models.CharField(max_length=100)
    explain_experience = models.CharField(max_length=220)
    pub_date = models.DateField(auto_now_add=True)



