# ✅ Robot Check Solution - User-Assisted Verification

## How It Works

The scraper now **pauses and waits for you** to complete any robot verification manually. This is the most reliable solution!

## Step-by-Step Guide

### When Using "Listing URL" Mode:

1. **Submit a Realtor.ca listing URL**
   ```
   https://www.realtor.ca/real-estate/[property-id]/[address]
   ```

2. **Browser window opens automatically**
   - A Chrome window will pop up
   - You'll see the page loading

3. **If robot check appears:**
   ```
   ┌─────────────────────────────────────────┐
   │  □ I'm not a robot                      │
   │                                         │
   │  [Click the checkbox or solve CAPTCHA]  │
   └─────────────────────────────────────────┘
   ```

   **→ Complete the verification**
   - Click "I'm not a robot"
   - Solve any image challenges
   - Wait for the listing page to load

4. **Scraper continues automatically**
   - Once the page loads, scraping starts
   - You'll see progress in the backend terminal
   - Browser window closes when done

## What You'll See

### In the Browser Window:
```
1. Page loads → Robot check appears (if detected)
2. You complete the verification
3. Listing page loads with photos
4. Scraper extracts images (you'll see scrolling)
5. Window closes
```

### In the Backend Terminal:
```
Opening browser and navigating to listing...

======================================================================
PLEASE COMPLETE HUMAN VERIFICATION IF PROMPTED
======================================================================
A browser window has opened. If you see a robot check or CAPTCHA:
  1. Complete the verification in the browser window
  2. Wait for the listing page to load
  3. The scraper will automatically continue

Waiting up to 60 seconds for page to be ready...
======================================================================

✓ Page loaded successfully!

Analyzing 10 images (out of 50 total)
Auditing image 1/10...
Auditing image 2/10...
...
```

## Timing

- **With robot check**: ~10-20 seconds (time to complete CAPTCHA)
- **Without robot check**: ~5-8 seconds
- **Timeout**: 60 seconds max (if you don't complete it in time)

## Benefits

✅ **Always works** - No anti-detection tricks needed
✅ **Reliable** - Real human verification
✅ **Simple** - Just click the checkbox
✅ **Fast** - Only takes a few seconds

## Alternative: Image URL Mode

If you don't want to deal with robot checks at all:

1. Click **"Image URL"** toggle button
2. Right-click on any property photo → "Copy Image Address"
3. Paste the URL
4. ✅ Instant analysis - no robot check possible!

## Troubleshooting

### "Timeout waiting for page elements"
- The robot check wasn't completed in 60 seconds
- The page structure might have changed
- **Solution**: Try again, or switch to Image URL mode

### Browser window closes immediately
- The scraper didn't detect a robot check
- Page loaded successfully without verification
- **This is normal!** Analysis continues automatically

### Can't see the browser window
- Check if it opened behind other windows
- Look for Chrome icon in taskbar/dock
- **Solution**: Click the Chrome icon to bring it forward

## Demo Flow

```
User: Pastes listing URL → Clicks "Analyze Property"
  ↓
Browser: Opens listing page
  ↓
Robot Check: "Are you human?"
  ↓
User: ✓ Completes verification
  ↓
Page: Loads with all photos
  ↓
Scraper: Extracts images → Audits each one
  ↓
Frontend: Shows results with property info
  ↓
User: Clicks on photo to generate renovation
```

## Best Practices for Demos

1. **Test before demo**: Run through once to see if robot checks appear
2. **Have backup ready**: Keep Image URL mode as fallback
3. **Be patient**: Wait for the browser window to open
4. **Don't close browser**: Let the scraper close it automatically

## Production Recommendations

For a production app, consider:
- Using a CAPTCHA solving service (e.g., 2Captcha)
- Implementing residential proxies
- Using Realtor.ca official API (if available)
- Rate limiting requests to avoid triggering checks

For this hackathon, **user-assisted verification is perfect** - it's reliable, simple, and demonstrates the full workflow!

---

**Ready to test?**

1. Start backend: `uvicorn main:app --reload`
2. Click "Listing URL" mode
3. Paste any Realtor.ca listing
4. Complete robot check if prompted
5. Watch the magic happen! ✨
