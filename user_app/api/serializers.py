from django.contrib.auth.models import User
from rest_framework import serializers

#registrations
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password',}, write_only = True )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']     
        # username,email & password are by default in Django, password2 is for confirm password and we neet to define this extra field in serilaizer
        extra_kwargs = {
                'password' : {'write_only':True}
        }

    #as we are using extra field password2, so we need to override save() function as password2 is not the default field
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'error':'password and confirm password doesn"t match'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'User already Exists'})
        
        #as we are overriding save(), we need to create the user manually
        account = User(email = self.validated_data['email'], username = self.validated_data['username'])
        account.set_password(password)
        account.save()

        return account