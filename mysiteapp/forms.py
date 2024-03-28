from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        #fields = '__all__'
        fields = ('first_name', 'last_name', 'username', 'email', 'age')