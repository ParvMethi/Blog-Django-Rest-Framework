from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from home.models import Blog
from home.serializer import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

class PublicBlog(APIView):
    def get(self, request):
        objs = Blog.objects.all().order_by('?')

        if request.GET.get('search'):
            search = request.GET.get('search')
            objs = objs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

        page_number = request.GET.get('page', 1)
        paginator = Paginator(objs, 5)
        serializer = BlogSerializer(paginator.page(page_number), many=True)
        
        return Response({'data':serializer.data, 'message':'All blogs fetched successfully'})
        

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get(self, request):
        objs = Blog.objects.filter(user = request.user)

        if request.GET.get('search'):
            search = request.GET.get('search')
            objs = objs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

        
        serializer = BlogSerializer(objs, many = True)
        return Response({'data':serializer.data, 'message':'blogs fetched successfully'})

    def post(self, request):
        data = request.data
        # print(request.user)
        data['user'] = request.user.id
        serializer = BlogSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'message':'blog created successfully'})
        return Response(serializer.errors)

    def patch(self, request):
        data = request.data

        blog = Blog.objects.filter(uid = data.get('uid'))

        if not blog.exists():
            return Response({'message':'invalid blog uid'})
        
        print(blog[0].user)

        if request.user != blog[0].user:
            return Response({'message' : 'you are not authorized to do this'}) 
        
        serializer = BlogSerializer(blog[0], data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
       
        return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data

        blog = Blog.objects.filter(uid = data.get('uid'))
        if not blog.exists():
            return Response({'message':'such blog not exists'})
        if request.user != blog[0].user:
             return Response({'message' : 'you are not authorized to delete this'}) 
        blog.delete()
        return Response({'message' : 'deleted successfully'})