const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: false }); 
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('https://dev261475.service-now.com/navpage.do');

    // Fill in the username
    await page.fill('input#user_name', 'admin'); 

    // Fill in the password
    await page.fill('input#user_password', '@Shyam2610'); // Replace 'your_password' with the actual password

    // Click the login button
    await page.click('button#sysverb_login');

    // Wait for navigation after login
    await page.waitForNavigation();

    // Optionally verify successful login
    if (page.url() !== 'https://dev261475.service-now.com/navpage.do') {
        console.log('Login successful!');
    } else {
        console.error('Login failed. Check credentials or page state.');
    }

    // Close the browser
    await browser.close();
})();
