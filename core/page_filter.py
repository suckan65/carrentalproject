from rest_framework.response import Response
import math

def pages_filter(self, request, Model, *args, **kwargs):
    page = request.query_params.get("page", 1)
    size = request.query_params.get("size", 10)
    sort = request.query_params.get("sort", "id")
    direction = request.query_params.get("direction", "asc")
            
    page = int(page)
    size = int(size)
            
    if page < 1:
        page = 1
                
    if size < 1:
        size = 1
                
    start_index = (page-1) * size
    end_index = (start_index + size)
            
    if direction.lower() == "asc":
        try:
            messages = Model.objects.order_by(sort)[start_index:end_index]
        except:
            messages = Model.objects.order_by(sort)[start_index]
                    
    else:
        try:
            messages = Model.objects.order_by(f"-{sort}")[start_index:end_index]
        except:
            messages = Model.objects.order_by(f"-{sort}")[start_index]
                    
                    
    serializer = self.serializer_class(messages, many=True)
    total_users = Model.objects.count()
    total_pages = math.ceil(total_users/size)
    num_elements = len(messages)
            
            
    data = {
        "totalElements": total_users,
        "totalPages": total_pages,
        "first":start_index + 1,
        "last": num_elements,
        "number": num_elements,
        "sort": {
            "sorted": True,
            "unsorted": False,
            "empty": False
        },
        "numberOfElements": num_elements,
        "pageable": {
            "sort": {
                "sorted": True,
                "unsorted": False,
                "empty": False  
            },
            "paged": True,
            "unpaged": False,
            "pageNumber": page,
            "pageSize": size,
            "offset": start_index
        },
        "size": size,
        "content": serializer.data,
        "empty": len(serializer.data) == 0
    }
            
    return Response(data)

