from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=64)
    cover = models.ImageField(upload_to='orders/images/', null=True)
    def __str__(self):
        return f"{self.name}"
        
class Regular_pizza(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)
    no_of_toppings=models.DecimalField(max_digits=4,decimal_places=0)
    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Sicilian_pizza(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)
    no_of_topping=models.DecimalField(max_digits=4,decimal_places=0)
    
    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Topping(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Pasta(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Salad(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Dinner_platter(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class Regular_pizza_order(models.Model):
    pizza = models.ForeignKey(Regular_pizza,on_delete=models.CASCADE, related_name="Pizza")