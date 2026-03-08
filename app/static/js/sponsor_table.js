 $(document).ready(function () {
    $('#sponsors-table').DataTable({
        ajax: 'api/sponsors',
        columns: [
            {data: 'name', render: (data, type, row) => {
                return '<a href="/sponsors/' + row.id + '">' + data + '</a>'
            }},
            {data: 'organization_classification', searchable: false, orderable: false, render: (data) => {
                return data[0].toUpperCase() + data.slice(1) + " House"
            }},
            {data: 'donation_count_all', searchable: false, render: (data) => {
                return new Intl.NumberFormat('en-US').format(data)
            }},
            {data: 'avg_donation_all', searchable: false, render: (data) => {
                return new Intl.NumberFormat('en-US', {
                            style: 'currency',
                            currency: 'USD',
                        }).format(data)
            }},
            {data: 'num_bills', searchable: false},
            {data: 'pct_bills_passed', searchable: false, render: (data) => {
                return new Intl.NumberFormat('en-US', {
                            style: 'percent',
                        }).format(data)
            }},
            {data: 'effectiveness_score', searchable: false, render: (data) => {
                score = parseInt(data * 100)
                colorClass = score > 65 ? "text-bg-success" : (score < 35 ? "text-bg-danger" : "text-bg-warning")
                return '<span class="badge '+colorClass+'">' + score + '</span>'
            }}
        ]
    });
});