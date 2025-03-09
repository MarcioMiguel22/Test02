from .models import RegistroEntrega

class RegistroEntregaService:
    @staticmethod
    def create_registro(data):
        """Create a new registro with business logic"""
        # Add any business logic here
        return RegistroEntrega.objects.create(**data)
        
    @staticmethod
    def get_registros_por_obra(obra_id):
        """Get registros filtered by obra_id"""
        return RegistroEntrega.objects.filter(obra_id=obra_id)
