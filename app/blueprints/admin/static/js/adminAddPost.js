const tagInput = document.querySelector('#tag-input');
const tagDisplay = document.querySelector('.tags-display');
const tagButton = document.querySelector('#tag-input-button');
const formElement = document.querySelector('#add-post-form');
var existingTags = window.existingTags || [];


const tagSet = new Set();


if (existingTags) {
    for (let tag of existingTags) {
        addTagToSet(tag);
    }
    renderTags()
}


formElement.addEventListener('submit', (event) =>{
    event.preventDefault()
    const hiddenInput = document.querySelector('#tags');

    hiddenInput.value = JSON.stringify([...tagSet]);

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