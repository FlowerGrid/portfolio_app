const tagInput = document.querySelector('#tag-input');
const tagDisplay = document.querySelector('.tags-display');
const tagButton = document.querySelector('#tag-input-button');
const formElement = document.querySelector('#add-post-form');
const addTextBtn = document.querySelector('#add-text-content-block');
const addImgBtn = document.querySelector('#add-image-content-block');
const contentBlockBtns = document.querySelector('.content-block-buttons');
const contentBlocksContainer = document.querySelector('.content-blocks-container');
const parentType = document.querySelector('#parent-type').dataset.model;
const parentId = document.querySelector('#id').value;
var existingTags = window.existingTags || [];


const tagSet = new Set();
const contentBlocks = []
let imgCounter = 1;


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
    contentBlocksHiddenInput.value = JSON.stringify(contentBlocks);

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
        // TODO
        // Check for presence of file input
        // URL.revokeObjectURL()

        let parentBlock = target.parentNode;
        if (parentBlock.dataset.objectUrl) {
            URL.revokeObjectURL(parentBlock.dataset.objectUrl);
        }
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
        let imgPreview;
        // Text Block Specific Stuff
        if (target.id === 'add-text-content-block') {
            blockLabel.textContent = 'Text Content';

            newBlockInput = document.createElement('textarea');
            batchSetAttributes(
                newBlockInput,
                {
                    'class': 'text-block content-block-input',
                    'data-content-type': 'text'
                }
            
            );
        } else if (target.id === 'add-image-content-block') {
            blockLabel.textContent = 'Upload Image';

            newBlockInput = document.createElement('input');
            batchSetAttributes (
                newBlockInput,
                {
                    'type': 'file',
                    'class': 'img-block content-block-input',
                    'accept': 'png, .jpg, .jpeg, .heic, .heif, image/png, image/jpeg, image/heic, image/heif',
                    'name': `image-${imgCounter}`,
                    'data-content-type': 'image'
                }
            );

            imgCounter ++;

            imgPreview = document.createElement('img');
            imgPreview.classList.add('img-preview')
        };

        // Add the elemnts to their conainers
        let kiddos = [blockLabel, newBlockInput, imgPreview, deleteBlockBtn]
        for (let kid of kiddos) {
            if (kid) {
                newContentBlock.appendChild(kid);
            }
        }

        contentBlocksContainer.append(newContentBlock);

    };
});

// Image Previews
document.addEventListener('change', (event) => {
    let target = event.target;
    if (target.classList.contains('img-block')) {

        const parentContainer = target.parentNode;
        if (parentContainer.dataset.objectUrl) {
            URL.revokeObjectURL(parentContainer.dataset.objectUrl)
        }

        const file = target.files[0];
        if (!file) return;

        const objectUrl = URL.createObjectURL(file);
        parentContainer.dataset.objectUrl = objectUrl;

        const preview = parentContainer.querySelector('.img-preview');
        preview.src = objectUrl;
    }
})


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


// Content Block Functions
function gatherContentBlockData() {
    let blocks = contentBlocksContainer.querySelectorAll('.content-block')
    let blockObjects = []
    let blockPos = 0

    for (let block of blocks) {

        let inputElement = block.querySelector('.content-block-input');

        let blockObj = {
            'parentType': parentType,
            'parentId': parentId || null,
            'imageName': inputElement.getAttribute('name') || null,
            'blockType': inputElement.dataset.contentType,
            'position': blockPos,
            'textContent': inputElement.value || null,
            
        };

        blockObjects.push(blockObj);
        blockPos++;
    }

}