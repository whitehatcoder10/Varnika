document.addEventListener('DOMContentLoaded', () => {
    // --- Get all the necessary elements from the HTML ---
    const textForm = document.getElementById('text-form');
    const descriptionEl = document.getElementById('description');
    const captionsEl = document.getElementById('captions');

    const imageForm = document.getElementById('image-form');
    const generatedImageEl = document.getElementById('generated-image');
    
    const API_BASE_URL = 'http://127.0.0.1:5000/api';

    // --- Text Generation Logic ---
    textForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the page from reloading
        const button = textForm.querySelector('button');
        button.disabled = true;
        button.textContent = 'Generating...';

        // Show a loading message
        descriptionEl.textContent = 'AI is crafting your content...';
        captionsEl.textContent = '';

        try {
            const productType = document.getElementById('product_type').value;
            const keywords = document.getElementById('keywords').value;

            const response = await fetch(`${API_BASE_URL}/generate_content`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_type: productType, keywords: keywords })
            });

            const data = await response.json();

            if (!response.ok || data.error) {
                throw new Error(data.error || 'Failed to generate content.');
            }

            // Update the page with the results
            descriptionEl.textContent = data.description;
            captionsEl.textContent = data.captions;
        } catch (error) {
            descriptionEl.textContent = 'An error occurred: ' + error.message;
            captionsEl.textContent = '';
        } finally {
            // Re-enable the button
            button.disabled = false;
            button.textContent = 'Generate Content';
        }
    });

    // --- Image Enhancement Logic ---
    imageForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the page from reloading
        const button = imageForm.querySelector('button');
        button.disabled = true;
        button.textContent = 'Enhancing...';

        // Hide old image and show a loading message in the 'alt' text
        generatedImageEl.style.display = 'block'; // Ensure the alt text is visible
        generatedImageEl.src = ''; // Clear the previous image
        generatedImageEl.alt = 'Generating enhanced image...';

        const fileInput = document.getElementById('image-upload');
        const imagePrompt = document.getElementById('image-prompt').value;
        
        // Create a FormData object to send the file
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);
        formData.append('prompt', imagePrompt);

        try {
            const response = await fetch(`${API_BASE_URL}/enhance_image`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (!response.ok || data.error) {
                throw new Error(data.error || 'Failed to enhance image.');
            }

            // Update the image source with the new URL
            generatedImageEl.src = data.image_url;
            generatedImageEl.alt = 'Enhanced Product Image';
        } catch (error) {
            generatedImageEl.src = '';
            generatedImageEl.alt = 'An error occurred: ' + error.message;
        } finally {
            // Re-enable the button
            button.disabled = false;
            button.textContent = 'Enhance Image';
        }
    });
});