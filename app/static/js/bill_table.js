 $(document).ready(function () {
    $('#bills-table').DataTable({
        ajax: 'api/bills',
        columns: [
            {data: 'id', searchable: false, orderable: false},
            {data: 'identifier', orderable: false, render: (data, type, row) => {
                return '<a href="/bills/' + row.id + '">' + data + '</a>'
            }}
        ]
    });
});