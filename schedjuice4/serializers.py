from rest_framework import serializers

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = (kwargs.pop('fields', None))
        read_only_fields = kwargs.pop("read_only_fields",None)
        excluded_fields = kwargs.pop("excluded_fields", None)
        

        if fields:
            fields = fields.split(",")
        
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        
        # Making some fields read-only based on permissions.
        if read_only_fields is not None:
            for i in read_only_fields:
                try:
                    self.fields[i].read_only=True
                except KeyError as e:
                    pass
        
        if excluded_fields is not None:
            try:
                for i in excluded_fields:
                    self.fields.pop(i)
            except KeyError:
                pass


def status_check(status, status_lst:list)->bool:
    if status:
        if status not in status_lst:
            return False
    return True