from rest_framework import viewsets
from personajes.models import caballo,vaquero,arma
from personajes.serealizers import CaballoSerializer,ArmaSerializer,VaqueroSerializer
from rest_framework.response import Response
from rest_framework import status

class CaballoViewSet(viewsets.ModelViewSet):
    queryset = caballo.objects.all()
    serializer_class = CaballoSerializer
    def destroy(self, request, *args, **kwargs):
        # Puedes agregar lógica antes de eliminar
        instance = self.get_object()
        # Aquí puedes agregar lógica adicional antes de eliminar
        instance.delete()  # Eliminar el objeto
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        # Lógica antes de actualizar
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Parcial (PATCH) o completo (PUT)
        if serializer.is_valid():
            serializer.save()  # Guardar cambios
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VaqueroViewSet(viewsets.ModelViewSet):
    queryset = vaquero.objects.all()
    serializer_class = VaqueroSerializer

    def update(self, request, *args, **kwargs):
    # Lógica antes de actualizar
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Parcial (PATCH) o completo (PUT)
    
        if serializer.is_valid():
        # Actualizar caballos
            nuevo_caballo_nombre = request.data.get('nuevo_caballo_nombre', None)
            if nuevo_caballo_nombre:
                instance.caballos.update(nombre=nuevo_caballo_nombre)  # Asegúrate de manejar la actualización de los caballos
        # Actualizar armas
            nueva_arma_nombre = request.data.get('nueva_arma_nombre', None)
            if nueva_arma_nombre:
                instance.armas.update(nombre=nueva_arma_nombre)  # Asegúrate de manejar la actualización de las armas
        
            serializer.save()  # Guardar cambios en el vaquero
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArmaViewSet(viewsets.ModelViewSet):
    queryset = arma.objects.all()
    serializer_class = ArmaSerializer
    def destroy(self, request, *args, **kwargs):
        # Puedes agregar lógica antes de eliminar
        instance = self.get_object()
        # Aquí puedes agregar lógica adicional antes de eliminar
        instance.delete()  # Eliminar el objeto
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        # Lógica antes de actualizar
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Parcial (PATCH) o completo (PUT)
        if serializer.is_valid():
            serializer.save()  # Guardar cambios
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)