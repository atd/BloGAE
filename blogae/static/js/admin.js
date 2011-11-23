var admin = {
    edit: function(a){},
    delete: function(a){
        $.ajax({
            url: '',
            type: 'DELETE',
            data: {k: a.value},
            success: function(data){
                //TODO: remove row
                alert(data.k);
            },
            dataType: 'json'
        });
    }
}
