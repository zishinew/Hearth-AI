# AccessiVision

> AI-Powered Real Estate Accessibility Visualizer

**DeltaHacks 26 Project** 🏠

AccessiVision analyzes real estate images to identify accessibility barriers and generates AI-powered renovation visualizations with cost estimates. Whether you're a property buyer, seller, or accessibility advocate, AccessiVision helps you visualize how any property can be made more accessible.

## ✨ Features

- **🔍 AI-Powered Analysis**: Uses Gemini 1.5 Pro to detect accessibility barriers in property images
- **🎨 Visual Renovation Preview**: Generates realistic before/after images using AI image generation
- **💰 Cost Estimation**: Provides detailed cost estimates for accessibility renovations
- **🏘️ Full Property Analysis**: Scrapes Realtor.ca listings to analyze entire properties
- **📸 Single Image Mode**: Analyze individual images without scraping
- **♿ Wheelchair Accessibility Focus**: Specialized analysis for wheelchair-accessible modifications
- **⚡ On-Demand Generation**: Generate renovations only for images you want to see (saves API costs!)
- **🚀 Fast & Efficient**: Optimized workflow to minimize API calls and processing time

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini 1.5 Pro** - AI-powered accessibility analysis
- **Gemini Image Generation** - AI image renovation generation
- **Playwright** - Web scraping for Realtor.ca listings
- **Python 3.10+**

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **React Compare Slider** - Before/after image comparison

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 18+ and npm/yarn/pnpm
- Google Gemini API key
- Playwright (for web scraping)

## 🚀 Getting Started

### Backend Setup

1. **Navigate to the backend directory:**
   cd deltahacks26/backend
   
