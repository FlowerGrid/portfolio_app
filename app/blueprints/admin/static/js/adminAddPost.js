const tagInput = document.querySelector('#tag-input');
const tagDisplay = document.querySelector('.tags-display');
const tagButton = document.querySelector('#tag-input-button');
const formElement = document.querySelector('#add-post-form');
const addTextBtn = document.querySelector('#add-text-content-block');
const addImgBtn = document.querySelector('#add-image-content-block');
const contentBlockBtns = document.querySelector('.content-block-buttons');
const contentBlocksContainer = document.querySelector('.content-blocks-container');
var existingTags = window.existingTags || [];


const tagSet = new Set();
const contentBlocks = []


if (existingTags) {
    for (let tag of existingTags) {
        addTagToSet(tag);
    }
    renderTags()
}


formElement.addEventListener('submit', (event) =>{
    event.preventDefault()
    const tagsHiddenInput = document.querySelector('#tags');
    const contentBlocksHiddenInput = document.querySelector('#content_blocks')

    tagsHiddenInput.value = JSON.stringify([...tagSet]);
    contentBlocksHiddenInput = JSON.stringify(contentBlocks);

    formElement.submit();
})

tagInput.addEventListener('keydown', (event) =>{
    if (event.key === 'Enter' && !event.repeat) {
        event.preventDefault();
        tagButton.click()
    }
})

tagButton.addEventListener('click', () => {
    if (tagInput.value) {
        let tagText = tagInput.value;
        addTagToSet(tagText);
        tagInput.value = null;
        renderTags()
    }
})


// Delete content block event listener
contentBlocksContainer.addEventListener('click', (event) => {
    let target = event.target;
    if (target.classList.contains('del-content-block-btn')) {
        let parentBlock = target.parentNode;
        contentBlocksContainer.removeChild(parentBlock);
    }
})


contentBlockBtns.addEventListener('click', (event) => {
    let target = event.target;
    if (target.classList.contains('add-content-btn')) {
        // create a new element
        let newContentBlock = document.createElement('div');
        newContentBlock.classList.toggle('content-block');

        // add a text input field into the element
        let blockLabel = document.createElement('h4');
    
        // add a delete content block button to the element
        let deleteBlockBtn = document.createElement('input')
        deleteBlockBtn.type = 'button'
        batchSetAttributes(
            deleteBlockBtn,
            {
                'class': 'button-styles del-content-block-btn',
                'value': 'Remove Block'
            }
        );

        let newBlockInput;
        // Text Block Specific Stuff
        if (target.id === 'add-text-content-block') {
            blockLabel.textContent = 'Text Content';

            newBlockInput = document.createElement('textarea');
            batchSetAttributes(
                newBlockInput,
                    {
                        'class': 'text-block',
                        'name': 'text-block'
                    }
            
            );
        } else if (target.id === 'add-image-content-block') {
            blockLabel.textContent = 'Upload Image';

            newBlockInput = document.createElement('input');
            batchSetAttributes (
                newBlockInput,
                {
                    'type': 'file',
                    'class': 'img-block',
                    'accept': 'image/*'
                }
            );
        };

        // Add the elemnts to their conainers
        let kiddos = [blockLabel, newBlockInput, deleteBlockBtn]
        for (let kid of kiddos) {
            newContentBlock.appendChild(kid);
        }

        contentBlocksContainer.append(newContentBlock);

    };
});


function batchSetAttributes(el, attrs) {
    for (const key in attrs) {
        el.setAttribute(key, attrs[key])
    }
}


function addTagToSet(tagText) {
        tagText = normalizeTag(tagText)
        tagSet.add(tagText);
}


function normalizeTag(tag) {
    return tag
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '_')
        .replace(/[^\w_]/g, '');
}


function displayTag(tag) {
    return tag
        .replace(/_/g, ' ')
        .replace(/\b\w/g, c => c.toUpperCase());
}


function renderTags() {
    tagDisplay.innerHTML = '';
    tagSet.forEach((tag) => {
        let newTag = document.createElement('li');
        newTag.classList.toggle('tag');

        let textSpan = document.createElement('span')
        textSpan.classList.toggle('tag-text')
        textSpan.textContent = displayTag(tag);

        let removeIcon = document.createElement('span');
        removeIcon.classList.toggle('remove-icon');
        removeIcon.textContent = '❌';

        newTag.append(textSpan, removeIcon)

        tagDisplay.appendChild(newTag);
    });
}


// Remove tags
tagDisplay.addEventListener('click', (event) => {
    let target = event.target;

    if (target.classList.contains('remove-icon')) {
        let siblingSpan = target.previousElementSibling;
        if (siblingSpan.classList.contains('tag-text')) {
            tagSet.delete(normalizeTag(siblingSpan.textContent));
            renderTags();
        }
    }
})