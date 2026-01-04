const objectssPreview = document.querySelector('.all-objects');

objectssPreview.addEventListener('click', (event) => {
    const target = event.target;
    const linkTag = target.previousElementSibling;

    if (target.classList.contains('toggle-active-button')) {
        const targetId = linkTag.dataset.objectId;
        const pageName = document.body.dataset.pageName


        console.log(targetId)

        fetch('/admin/toggle-active-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                target_id: targetId,
                page_name: pageName
            })
        })
        .then (response => response.json())
        .then (data => {
            if (data.success) {
                linkTag.dataset.isActive = data.new_status;
                if (data.new_status) {
                    target.classList.add('active-project');
                } else {
                    target.classList.remove('active-project');
                }
            }
        })

    }
})