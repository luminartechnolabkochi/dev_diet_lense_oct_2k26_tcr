from django.shortcuts import render

# Create your views here.


from rest_framework.generics import DestroyAPIView,ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView

from diet_app.serializers import UserSerializer,UserProfileSerializer,FoodLogSerializer

from rest_framework import permissions,authentication

from rest_framework.views import APIView

from diet_app.utility_fun import daily_calorie_consumption

from diet_app.permissions import IsOwner

from diet_app.models import UserProfile,User,FoodLog


class SignUpView(CreateAPIView):

    serializer_class = UserSerializer


class UserProfileCreateView(CreateAPIView):

    serializer_class = UserProfileSerializer

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):

        # validated_data = serializer.validated_data

        # cal = daily_calorie_consumption(height=validated_data.get("height"),
        #                                 weight=validated_data.get("weight"),
        #                                 age=validated_data.get("age"),
        #                                 gender=validated_data.get("gender"),
        #                                 activity_level=float(validated_data.get("activity_level",1.2))
        #                                 )

        
        serializer.save(owner=self.request.user)

class UserProfileRetrieveUpdateView(RetrieveAPIView,UpdateAPIView):

    serializer_class = UserProfileSerializer

    authentication_classes =[authentication.TokenAuthentication]

    permission_classes =[IsOwner]

    queryset=UserProfile.objects.all()


class UserDetailView(RetrieveAPIView):

    serializer_class = UserSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

    queryset=User.objects.all()


class FoodLodAddListView(CreateAPIView,ListAPIView):

    serializer_class = FoodLogSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):

        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        
        return FoodLog.objects.filter(owner =  self.request.user)
    

class FoodLogRetrieveUpdateDestroyView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):


    serializer_class = FoodLogSerializer

    queryset = FoodLog.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[IsOwner]


from django.utils import timezone

from rest_framework.response import Response

from django.db.models import Sum

class SummaryView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):

        cur_date = timezone.now().date()

        qs = FoodLog.objects.filter(owner = request.user,created_at__date=cur_date)

        total_consumed=qs.values("calories").aggregate(total=Sum("calories"))
        # total_consumed={"total":325}
        context={
            "daily_target":request.user.profile.bmr,

            "total_consumed":total_consumed.get("total",0),
            
            "balance":request.user.profile.bmr - total_consumed.get("total",0)
        }

        return Response(data=context)