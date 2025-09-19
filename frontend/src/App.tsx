import React, { useEffect, useState } from 'react';
import { Routes, Route, Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './components/ui/dialog';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Textarea } from './components/ui/textarea';
import { Badge } from './components/ui/badge';
import { ImageWithFallback } from './components/figma/ImageWithFallback';
import varnikaLogo from 'figma:asset/5b309230f699c8cd589799542daefe756406677e.png';
import backgroundImage from 'figma:asset/f865fe46b7f602ddc489cac1f1fca444b9fce593.png';
import { Heart, ShoppingCart, Upload, Plus, Minus, Play, User, Package, Info, Home, LogOut, Loader2 } from 'lucide-react';
import { apiService, Product as ApiProduct } from './services/api';

type UserType = 'seller' | 'buyer' | null;

interface Product {
  id: number;
  name: string;
  price: number;
  description: string;
  image: string;
  category: string;
  seller: string;
}

interface CartItem extends Product {
  quantity: number;
}

const App = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [userType, setUserType] = useState<UserType>(null);
  const [showLogin, setShowLogin] = useState(false);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [description, setDescription] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [enhancedImageUrl, setEnhancedImageUrl] = useState<string | null>(null);
  const [isEnhancingImage, setIsEnhancingImage] = useState(false);
  const [aiGeneratedContent, setAiGeneratedContent] = useState<{
    description: string;
  } | null>(null);
  const [isGeneratingContent, setIsGeneratingContent] = useState(false);
  const [showSuccessMessage, setShowSuccessMessage] = useState(false);

  const categories = [
    { name: 'Pottery', image: 'https://images.unsplash.com/photo-1695746999130-17bc94e000e8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwb3R0ZXJ5JTIwaGFuZGljcmFmdCUyMGNlcmFtaWN8ZW58MXx8fHwxNzU4MjAyOTM0fDA&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Textiles', image: 'https://images.unsplash.com/photo-1719462211900-3d4c1a62cae4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZXh0aWxlJTIwd2VhdmluZyUyMGhhbmRpY3JhZnR8ZW58MXx8fHwxNzU4MjAyOTM1fDA&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Woodwork', image: 'https://images.unsplash.com/photo-1603789766884-aef036cd3b5a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b29kd29yayUyMGhhbmRpY3JhZnQlMjBjYXJ2aW5nfGVufDF8fHx8MTc1ODIwMjkzNXww&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Jewelry', image: 'https://images.unsplash.com/photo-1717917197052-fda91a7e003c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxqZXdlbHJ5JTIwaGFuZGljcmFmdCUyMHRyYWRpdGlvbmFsfGVufDF8fHx8MTc1ODIwMjkzNnww&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Embroidery', image: 'https://images.unsplash.com/photo-1657470036063-c7e49da31393?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxlbWJyb2lkZXJ5JTIwaGFuZGljcmFmdCUyMHRleHRpbGV8ZW58MXx8fHwxNzU4MjAyOTM2fDA&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Basketry', image: 'https://images.unsplash.com/photo-1617191598003-fa321e7e425b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiYXNrZXQlMjB3ZWF2aW5nJTIwaGFuZGljcmFmdHxlbnwxfHx8fDE3NTgyMDI5MzZ8MA&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Leather', image: 'https://images.unsplash.com/photo-1543874835-ad7d64196a07?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsZWF0aGVyJTIwaGFuZGljcmFmdCUyMHRyYWRpdGlvbmFsfGVufDF8fHx8MTc1ODIwMjkzN3ww&ixlib=rb-4.1.0&q=80&w=300' },
    { name: 'Metalwork', image: 'https://images.unsplash.com/photo-1638256049300-d5fbdae0e8c7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXRhbCUyMGhhbmRpY3JhZnQlMjBjcmFmdHxlbnwxfHx8fDE3NTgyMDI5Mzd8MA&ixlib=rb-4.1.0&q=80&w=300' }
  ];

  // Load products from API
  const loadProducts = async (category?: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.getProducts(category);
      if (response.success && response.data) {
        const apiProducts = response.data.products.map((apiProduct: ApiProduct) => ({
          id: apiProduct.product_id,
          name: apiProduct.name,
          price: apiProduct.price,
          description: apiProduct.ai_description || apiProduct.description || '',
          image: apiProduct.image_url || '',
          category: apiProduct.category || 'General',
          seller: apiProduct.artisan_name || 'Unknown Artisan'
        }));
        setProducts(apiProducts);
      } else {
        // If API fails, show fallback products instead of error
        console.warn('API failed, showing fallback products:', response.error);
        setProducts(getFallbackProducts());
      }
    } catch (err) {
      // If network fails, show fallback products instead of error
      console.warn('Network error, showing fallback products:', err);
      setProducts(getFallbackProducts());
    } finally {
      setLoading(false);
    }
  };

  // Fallback products for when API is not available
  const getFallbackProducts = (): Product[] => [
    {
      id: 1,
      name: 'Handcrafted Ceramic Vase',
      price: 85,
      description: 'Beautiful handmade ceramic vase with traditional glazing techniques, perfect for home decor.',
      image: 'https://images.unsplash.com/photo-1695746999130-17bc94e000e8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwb3R0ZXJ5JTIwaGFuZGljcmFmdCUyMGNlcmFtaWN8ZW58MXx8fHwxNzU4MjAyOTM0fDA&ixlib=rb-4.1.0&q=80&w=400',
      category: 'Pottery',
      seller: 'Maya Crafts'
    },
    {
      id: 2,
      name: 'Woven Cotton Scarf',
      price: 45,
      description: 'Soft cotton scarf with intricate woven patterns, handcrafted using traditional techniques.',
      image: 'https://images.unsplash.com/photo-1719462211900-3d4c1a62cae4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZXh0aWxlJTIwd2VhdmluZyUyMGhhbmRpY3JhZnR8ZW58MXx8fHwxNzU4MjAyOTM1fDA&ixlib=rb-4.1.0&q=80&w=400',
      category: 'Textiles',
      seller: 'Heritage Weavers'
    },
    {
      id: 3,
      name: 'Carved Wooden Bowl',
      price: 65,
      description: 'Hand-carved wooden bowl made from sustainable wood with intricate traditional patterns.',
      image: 'https://images.unsplash.com/photo-1603789766884-aef036cd3b5a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b29kd29yayUyMGhhbmRpY3JhZnQlMjBjYXJ2aW5nfGVufDF8fHx8MTc1ODIwMjkzNXww&ixlib=rb-4.1.0&q=80&w=400',
      category: 'Woodwork',
      seller: 'Forest Artisans'
    }
  ];

  const stories = [
    {
      name: 'Priya Sharma',
      craft: 'Pottery',
      story: 'From a small village in Rajasthan, Priya learned pottery from her grandmother. Through Varnika, she now sells her beautiful ceramic pieces worldwide.',
      image: 'https://images.unsplash.com/photo-1716876995651-1ff85b65a6d9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhcnRpc2FuJTIwd29ya2luZyUyMGhhbmRpY3JhZnR8ZW58MXx8fHwxNzU4MjAyOTM4fDA&ixlib=rb-4.1.0&q=80&w=400'
    },
    {
      name: 'Arjun Kumar',
      craft: 'Woodwork',
      story: 'A master craftsman from Kerala, Arjun creates intricate wooden sculptures. Varnika helped him reach customers who appreciate traditional art.',
      image: 'https://images.unsplash.com/photo-1603789766884-aef036cd3b5a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b29kd29yayUyMGhhbmRpY3JhZnQlMjBjYXJ2aW5nfGVufDF8fHx8MTc1ODIwMjkzNXww&ixlib=rb-4.1.0&q=80&w=400'
    },
    {
      name: 'Meera Devi',
      craft: 'Textiles',
      story: 'A weaver from Gujarat with 30 years of experience, Meera creates stunning handloom textiles. Her family tradition continues through Varnika.',
      image: 'https://images.unsplash.com/photo-1719462211900-3d4c1a62cae4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZXh0aWxlJTIwd2VhdmluZyUyMGhhbmRpY3JhZnR8ZW58MXx8fHwxNzU4MjAyOTM1fDA&ixlib=rb-4.1.0&q=80&w=400'
    }
  ];

  const addToCart = (product: Product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => 
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId: number) => {
    setCart(prev => prev.filter(item => item.id !== productId));
  };

  const updateQuantity = (productId: number, newQuantity: number) => {
    if (newQuantity === 0) {
      removeFromCart(productId);
      return;
    }
    setCart(prev => 
      prev.map(item => 
        item.id === productId 
          ? { ...item, quantity: newQuantity }
          : item
      )
    );
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const getTotalItems = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
    setShowLogin(false);
    navigate('/home');
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserType(null);
    setCart([]);
    setSelectedCategory(null);
    navigate('/');
  };

  // Load products when category changes
  useEffect(() => {
    if (isLoggedIn) {
      loadProducts(selectedCategory || undefined);
    }
  }, [selectedCategory, isLoggedIn]);

  const renderNavigation = () => {
    const pathname = location.pathname;
    if (!isLoggedIn || pathname === '/' || pathname === '/join') return null;

    return (
      <nav className="bg-[#0A2647] text-white p-3 md:p-4 flex flex-col md:flex-row justify-between items-start md:items-center space-y-2 md:space-y-0">
        <div className="flex items-center space-x-2 md:space-x-4">
          <img src={varnikaLogo} alt="Varnika" className="h-6 w-6 md:h-8 md:w-8" />
          <h1 className="text-lg md:text-xl font-bold">Varnika</h1>
        </div>
        <div className="flex flex-wrap items-center gap-2 md:gap-4 text-sm md:text-base">
          <Link to="/home" onClick={() => setSelectedCategory(null)}>
            <Button 
              variant="ghost" 
              size="sm"
              className="text-white hover:bg-[#144272] p-2"
            >
              <Home className="w-4 h-4 md:mr-2" />
              <span className="hidden md:inline">Home</span>
            </Button>
          </Link>
          {userType === 'seller' && (
            <Link to="/add-product">
              <Button 
                variant="ghost" 
                size="sm"
                className="text-white hover:bg-[#144272] p-2"
              >
                <Plus className="w-4 h-4 md:mr-2" />
                <span className="hidden md:inline">Add Product</span>
              </Button>
            </Link>
          )}
          {userType === 'buyer' && (
            <Link to="/cart">
              <Button 
                variant="ghost" 
                size="sm"
                className="text-white hover:bg-[#144272] relative p-2"
              >
                <ShoppingCart className="w-4 h-4 md:mr-2" />
                <span className="hidden md:inline">Cart ({getTotalItems()})</span>
                <span className="md:hidden">({getTotalItems()})</span>
              </Button>
            </Link>
          )}
          <Link to="/about">
            <Button 
              variant="ghost" 
              size="sm"
              className="text-white hover:bg-[#144272] p-2"
            >
              <Info className="w-4 h-4 md:mr-2" />
              <span className="hidden md:inline">About</span>
            </Button>
          </Link>
          <Button 
            variant="ghost" 
            size="sm"
            className="text-white hover:bg-[#144272] p-2"
            onClick={handleLogout}
          >
            <LogOut className="w-4 h-4 md:mr-2" />
            <span className="hidden md:inline">Logout</span>
          </Button>
        </div>
      </nav>
    );
  };

  const renderLandingPage = () => (
    <div
      className="min-h-screen relative overflow-hidden"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      {/* Animated gradient veil */}
      <div className="absolute inset-0 animated-gradient opacity-80"></div>

      {/* Floating orbs */}
      <div className="orb orb-1"></div>
      <div className="orb orb-2"></div>
      <div className="orb orb-3"></div>

      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-4 md:p-8">
        <div className="glass-card w-full max-w-[calc(100%-2rem)] md:w-fit text-center p-6 md:p-8 rounded-xl">
          <img src={varnikaLogo} alt="Varnika" className="h-16 w-16 md:h-24 md:w-24 mx-auto mb-4 md:mb-6 fade-in-up" />
          <h1 className="text-gradient-animate text-4xl md:text-6xl font-bold mb-3 md:mb-4 fade-in-up delay-1">
            Welcome to Varnika
          </h1>
          <p className="typewriter text-[#0A2647] text-base md:text-xl mb-6 md:mb-8 max-w-2xl mx-auto">
            Where timeless craftsmanship meets the modern world.
          </p>
          <div className="inline-flex flex-col md:flex-row items-center gap-4 fade-in-up delay-2">
            <Link to="/join">
              <Button className="btn-shimmer px-6 py-3 md:px-8 md:py-4 text-base md:text-lg">
                Get Started
              </Button>
            </Link>
            <Link to="/home">
              <Button variant="outline" className="btn-ghost-glass px-6 py-3 md:px-8 md:py-4 text-base md:text-lg">
                Explore Products
              </Button>
            </Link>
          </div>
        </div>

        {/* Bottom teaser stats */}
        <div className="mt-8 md:mt-12 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 w-full max-w-6xl px-2 fade-in-up delay-3">
          <div className="stat-tile">
            <span className="stat-number">10k+</span>
            <span className="stat-label">Artisan Products</span>
          </div>
          <div className="stat-tile">
            <span className="stat-number">120+</span>
            <span className="stat-label">Communities</span>
          </div>
          <div className="stat-tile sm:col-start-2 md:col-start-auto">
            <span className="stat-number">100%</span>
            <span className="stat-label">Authentic Craft</span>
          </div>
        </div>
      </div>

      {/* Scroll cue */}
      <div className="scroll-cue">
        <span></span>
      </div>
    </div>
  );

  const renderUserSelect = () => (
    <div className="min-h-screen bg-white flex items-center justify-center p-4 md:p-8">
      <div className="text-center max-w-4xl">
        <h2 className="text-2xl md:text-4xl mb-4 md:mb-8 text-[#0A2647]">Join Varnika</h2>
        <p className="text-base md:text-lg text-[#144272] mb-8 md:mb-12">Choose your role and get started</p>
        
        <div className="flex flex-col md:flex-row space-y-6 md:space-y-0 md:space-x-8">
          <Card className="w-full md:w-80 cursor-pointer hover:shadow-lg transition-shadow border-[#205295]" 
                onClick={() => { setUserType('seller'); setShowLogin(true); }}>
            <CardHeader className="text-center">
              <User className="w-8 md:w-12 h-8 md:h-12 mx-auto mb-4 text-[#205295]" />
              <CardTitle className="text-[#0A2647] text-lg md:text-xl">Continue as Seller</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-[#144272] text-sm md:text-base">Showcase your handicrafts to a global audience. Add products, manage inventory, and grow your business.</p>
              <Button className="w-full mt-4 bg-[#205295] hover:bg-[#144272]">
                Get Started
              </Button>
            </CardContent>
          </Card>

          <Card className="w-full md:w-80 cursor-pointer hover:shadow-lg transition-shadow border-[#2C74B3]" 
                onClick={() => { setUserType('buyer'); setShowLogin(true); }}>
            <CardHeader className="text-center">
              <ShoppingCart className="w-8 md:w-12 h-8 md:h-12 mx-auto mb-4 text-[#2C74B3]" />
              <CardTitle className="text-[#0A2647] text-lg md:text-xl">Continue as Buyer</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-[#144272] text-sm md:text-base">Discover authentic handicrafts from talented artisans. Support traditional crafts and find unique pieces.</p>
              <Button className="w-full mt-4 bg-[#2C74B3] hover:bg-[#205295]">
                Get Started
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );

  const renderLoginModal = () => (
    <Dialog open={showLogin} onOpenChange={setShowLogin}>
      <DialogContent className="sm:max-w-md mx-4" aria-describedby="login-description">
        <DialogHeader>
          <DialogTitle className="text-[#0A2647] text-lg md:text-xl">Welcome to Varnika</DialogTitle>
        </DialogHeader>
        <div id="login-description" className="space-y-4">
          <div>
            <Label htmlFor="email" className="text-sm md:text-base">Email</Label>
            <Input id="email" type="email" placeholder="Enter your email" className="text-sm md:text-base" />
          </div>
          <div>
            <Label htmlFor="password" className="text-sm md:text-base">Password</Label>
            <Input id="password" type="password" placeholder="Enter your password" className="text-sm md:text-base" />
          </div>
          <Button 
            onClick={handleLogin} 
            className="w-full bg-[#205295] hover:bg-[#144272] text-sm md:text-base"
          >
            Login
          </Button>
          <p className="text-center text-xs md:text-sm text-[#144272]">
            Don't have an account? <span className="text-[#205295] cursor-pointer">Sign up</span>
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );

  const renderHomePage = () => (
    <div className="min-h-screen bg-gray-50">
      {renderNavigation()}
      
      <div className="p-4 md:p-6">
        {/* Categories Section */}
        <section className="mb-8 md:mb-12">
          <div className="flex flex-col md:flex-row justify-between items-center mb-4 md:mb-6">
            <h2 className="text-xl md:text-3xl mb-2 md:mb-0 text-[#0A2647]">Explore Categories</h2>
            {selectedCategory && (
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => setSelectedCategory(null)}
                className="text-[#205295] border-[#205295]"
              >
                Show All
              </Button>
            )}
          </div>
          <div className="flex space-x-3 md:space-x-4 overflow-x-auto pb-4 scrollbar-hide">
            {categories.map((category, index) => (
              <div 
                key={index} 
                className="flex-shrink-0 text-center cursor-pointer transition-transform hover:scale-105 focus:outline-none category-item"
                onClick={() => setSelectedCategory(category.name)}
              >
                <div className={`w-20 h-20 md:w-32 md:h-32 rounded-full overflow-hidden mb-2 md:mb-3 border-2 md:border-4 transition-all ${
                  selectedCategory === category.name 
                    ? 'border-[#2C74B3] shadow-lg scale-105' 
                    : 'border-[#205295]'
                }`}>
                  <ImageWithFallback 
                    src={category.image} 
                    alt={category.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <p className={`text-xs md:text-base transition-colors ${
                  selectedCategory === category.name ? 'text-[#2C74B3] font-semibold' : 'text-[#0A2647]'
                }`}>
                  {category.name}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Products Section */}
        <section className="mb-8 md:mb-12">
          <div className="flex items-center justify-between mb-4 md:mb-6">
            <h2 className="text-xl md:text-3xl text-[#0A2647]">
              {selectedCategory ? `${selectedCategory} Products` : 'Featured Products'}
            </h2>
            {products.length > 0 && products[0].id <= 3 && (
              <div className="text-xs text-[#144272] bg-yellow-50 px-2 py-1 rounded border border-yellow-200">
                📡 Demo Mode
              </div>
            )}
          </div>
          
          {loading ? (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-[#205295]" />
              <span className="ml-2 text-[#144272]">Loading products...</span>
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-12">
              <Package className="w-16 h-16 mx-auto mb-4 text-[#205295]" />
              <p className="text-[#144272] text-lg">No products found</p>
              {userType === 'seller' && (
                <Link to="/add-product">
                  <Button className="mt-4 bg-[#205295] hover:bg-[#144272]">
                    Add Your First Product
                  </Button>
                </Link>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
              {products.map((product) => (
                <Card key={product.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="h-40 md:h-48 overflow-hidden">
                    <ImageWithFallback 
                      src={product.image} 
                      alt={product.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <CardContent className="p-3 md:p-4">
                    <h3 className="text-base md:text-lg text-[#0A2647] mb-2 line-clamp-1">{product.name}</h3>
                    <p className="text-[#144272] text-xs md:text-sm mb-3 line-clamp-2">{product.description}</p>
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-lg md:text-2xl text-[#205295] font-bold">${product.price}</span>
                      <Badge variant="secondary" className="bg-[#2C74B3] text-white text-xs">
                        {product.category}
                      </Badge>
                    </div>
                    <p className="text-xs md:text-sm text-[#144272] mb-3">by {product.seller}</p>
                    {userType === 'buyer' && (
                      <Button 
                        onClick={() => addToCart(product)}
                        className="w-full bg-[#205295] hover:bg-[#144272] text-xs md:text-sm"
                        size="sm"
                      >
                        <ShoppingCart className="w-3 h-3 md:w-4 md:h-4 mr-1 md:mr-2" />
                        Add to Cart
                      </Button>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </section>

        {/* Stories Section */}
        <section>
          <h2 className="text-xl md:text-3xl mb-4 md:mb-6 text-[#0A2647] text-center">Artisan Stories</h2>
          <p className="text-center text-[#144272] mb-8 md:mb-12 text-sm md:text-base">Meet the talented craftspeople behind Varnika</p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 max-w-6xl mx-auto">
            {stories.map((story, index) => (
              <Card key={index} className="overflow-hidden">
                <div className="h-48 md:h-64 overflow-hidden">
                  <ImageWithFallback 
                    src={story.image} 
                    alt={story.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <CardContent className="p-4 md:p-6">
                  <h3 className="text-lg md:text-xl text-[#0A2647] mb-2">{story.name}</h3>
                  <Badge className="mb-4 bg-[#2C74B3] text-white text-xs">{story.craft}</Badge>
                  <p className="text-[#144272] leading-relaxed text-sm md:text-base">{story.story}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </div>
  );

  const startVoiceInput = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setDescription(prev => prev + transcript);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
    } else {
      alert('Speech recognition not supported in this browser');
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const enhanceImage = async () => {
    if (!selectedImage) return;
    
    setIsEnhancingImage(true);
    try {
      const response = await apiService.enhanceImage(selectedImage);
      if (response.success && response.data) {
        setEnhancedImageUrl(response.data.image_url);
      } else {
        setError(response.error || 'Failed to enhance image');
      }
    } catch (err) {
      setError('Failed to enhance image');
      console.error('Error enhancing image:', err);
    } finally {
      setIsEnhancingImage(false);
    }
  };

  const generateAIContent = async (category: string, description: string) => {
    if (!category || !description.trim()) {
      setError('Please select a category and enter a description first');
      return;
    }

    setIsGeneratingContent(true);
    setError(null);
    try {
      const response = await apiService.generateContent(category, description);
      if (response.success && response.data) {
        setAiGeneratedContent({
          description: response.data.description
        });
        // Don't automatically update the description - let user choose
      } else {
        setError(response.error || 'Failed to generate AI content');
      }
    } catch (err) {
      setError('Failed to generate AI content');
      console.error('Error generating AI content:', err);
    } finally {
      setIsGeneratingContent(false);
    }
  };

  const addProduct = async (productData: {
    name: string;
    price: number;
    category: string;
    description: string;
  }) => {
    setLoading(true);
    try {
      // Use the original image (backend will enhance it automatically)
      const imageUrl = imagePreview || '';
      const response = await apiService.addProduct({
        ...productData,
        image_url: imageUrl,
        artisan_id: 1 // Default artisan for demo
      });
      
      if (response.success) {
        // Show success message
        setShowSuccessMessage(true);
        setError(null);
        
        // Clear form
        setDescription('');
        setSelectedImage(null);
        setImagePreview(null);
        setEnhancedImageUrl(null);
        setAiGeneratedContent(null);
        
        // Reload products to show the new one
        await loadProducts(selectedCategory || undefined);
        
        // Redirect to products page after 2 seconds
        setTimeout(() => {
          setShowSuccessMessage(false);
          // Navigate to home page to show products
          window.location.href = '/';
        }, 2000);
      } else {
        setError(response.error || 'Failed to add product');
      }
    } catch (err) {
      setError('Failed to add product');
      console.error('Error adding product:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderAddProduct = () => {
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      const formData = new FormData(e.target as HTMLFormElement);
      const productData = {
        name: formData.get('productName') as string,
        price: parseFloat(formData.get('price') as string),
        category: formData.get('category') as string,
        description: description
      };
      
      if (!productData.name || !productData.price || !productData.category) {
        setError('Please fill in all required fields');
        return;
      }
      
      await addProduct(productData);
    };

    return (
      <div className="min-h-screen bg-gray-50">
        {renderNavigation()}
        
        <div className="p-4 md:p-6 max-w-2xl mx-auto">
          <h2 className="text-2xl md:text-3xl mb-4 md:mb-6 text-[#0A2647]">Add New Product</h2>
          
          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}
          
          {showSuccessMessage && (
            <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
              <div className="flex items-center">
                <div className="text-green-500 mr-3">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold">🎉 Product Added Successfully!</h3>
                  <p className="text-sm">Your product has been added with AI-enhanced description and image. Redirecting to products page...</p>
                </div>
              </div>
            </div>
          )}
          
          <Card>
            <CardContent className="p-4 md:p-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="productName" className="text-sm md:text-base">Product Name *</Label>
                  <Input 
                    id="productName" 
                    name="productName"
                    placeholder="Enter product name" 
                    className="text-sm md:text-base" 
                    required 
                  />
                </div>
                
                <div>
                  <Label htmlFor="price" className="text-sm md:text-base">Price ($) *</Label>
                  <Input 
                    id="price" 
                    name="price"
                    type="number" 
                    step="0.01"
                    placeholder="Enter price" 
                    className="text-sm md:text-base" 
                    required 
                  />
                </div>
                
                <div>
                  <Label htmlFor="category" className="text-sm md:text-base">Category *</Label>
                  <select 
                    className="w-full p-2 border rounded text-sm md:text-base" 
                    id="category"
                    name="category"
                    required
                  >
                    <option value="">Select a category</option>
                    {categories.map(cat => (
                      <option key={cat.name} value={cat.name}>{cat.name}</option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <Label htmlFor="description" className="text-sm md:text-base">Description</Label>
                    <div className="flex items-center space-x-2 text-xs text-[#144272]">
                      <span>AI-powered sales-optimized description</span>
                      <span className="text-green-600">✨</span>
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex space-x-2">
                      <Textarea 
                        id="description" 
                        name="description"
                        placeholder="Describe your product... (e.g., 'Handmade ceramic vase with blue patterns, traditional techniques, perfect for home decor')"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        className="flex-1 text-sm md:text-base min-h-[100px]"
                        rows={4}
                      />
                      <div className="flex flex-col space-y-2">
                        <Button 
                          type="button" 
                          onClick={startVoiceInput}
                          size="sm"
                          className={`px-3 py-2 ${isListening ? 'bg-red-500' : 'bg-[#205295]'} hover:bg-[#144272] text-white`}
                          disabled={isListening}
                          title="Voice Input"
                        >
                          {isListening ? '🔴' : '🎤'}
                        </Button>
                        <Button 
                          type="button" 
                          onClick={() => {
                            const category = (document.getElementById('category') as HTMLSelectElement)?.value;
                            generateAIContent(category, description);
                          }}
                          size="sm"
                          disabled={isGeneratingContent || !description.trim()}
                          className={`px-3 py-2 text-white ${
                            isGeneratingContent 
                              ? 'bg-gray-400 cursor-not-allowed' 
                              : 'bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700'
                          }`}
                          title="Preview AI Description (Auto-generated when adding product)"
                        >
                          {isGeneratingContent ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            '✨'
                          )}
                        </Button>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500">
                      💡 AI will automatically generate a compelling description when you add the product
                    </p>
                  </div>
                  {isListening && (
                    <p className="text-xs md:text-sm text-[#205295] mt-1">Listening... Speak now!</p>
                  )}
                  
                  {/* AI Generated Content Display */}
                  {aiGeneratedContent && (
                    <div className="mt-6 p-4 bg-gradient-to-r from-green-50 via-blue-50 to-purple-50 border border-green-200 rounded-lg shadow-sm">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                          <h4 className="text-sm font-semibold text-[#0A2647] flex items-center">
                            ✨ AI-Enhanced Description Preview
                          </h4>
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                            Ready
                          </span>
                        </div>
                        <Button
                          type="button"
                          size="sm"
                          variant="outline"
                          onClick={() => setAiGeneratedContent(null)}
                          className="text-xs hover:bg-red-50 hover:border-red-200"
                        >
                          ✕
                        </Button>
                      </div>
                      
                      <div className="space-y-4">
                        <div>
                          <Label className="text-xs font-medium text-[#144272] mb-2 block flex items-center">
                            <span className="w-1 h-1 bg-green-500 rounded-full mr-2"></span>
                            Compelling Product Description:
                          </Label>
                          <div className="p-4 bg-white rounded-lg border border-gray-200 text-sm text-[#0A2647] leading-relaxed shadow-sm">
                            {aiGeneratedContent.description}
                          </div>
                          <div className="mt-2 text-xs text-[#144272] flex items-center">
                            <span className="w-1 h-1 bg-blue-500 rounded-full mr-2"></span>
                            This description is optimized for sales and customer engagement
                          </div>
                        </div>
                        
                        <div className="flex flex-wrap gap-2 pt-2 border-t border-gray-200">
                          <Button
                            type="button"
                            size="sm"
                            onClick={() => setDescription(aiGeneratedContent.description)}
                            className="text-xs bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white"
                          >
                            ✨ Use This Description
                          </Button>
                          <Button
                            type="button"
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              setDescription(prev => prev + '\n\n' + aiGeneratedContent.description);
                            }}
                            className="text-xs hover:bg-blue-50 hover:border-blue-200"
                          >
                            📝 Add to Current
                          </Button>
                          <Button
                            type="button"
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              navigator.clipboard.writeText(aiGeneratedContent.description);
                              alert('Description copied to clipboard!');
                            }}
                            className="text-xs hover:bg-purple-50 hover:border-purple-200"
                          >
                            📋 Copy
                          </Button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                
                <div>
                  <Label htmlFor="image" className="text-sm md:text-base">Product Image</Label>
                  <div className="border-2 border-dashed border-[#205295] rounded-lg p-6 md:p-8 text-center">
                    {imagePreview ? (
                      <div className="space-y-4">
                        <img 
                          src={imagePreview} 
                          alt="Preview" 
                          className="max-h-48 mx-auto rounded"
                        />
                        <div className="space-x-2">
                          <Button 
                            type="button"
                            variant="outline" 
                            size="sm"
                            onClick={enhanceImage}
                            disabled={isEnhancingImage}
                            className="text-sm md:text-base"
                          >
                            {isEnhancingImage ? (
                              <>
                                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                                Enhancing...
                              </>
                            ) : (
                              'Preview Enhancement'
                            )}
                          </Button>
                          <Button 
                            type="button"
                            variant="outline" 
                            size="sm"
                            onClick={() => {
                              setSelectedImage(null);
                              setImagePreview(null);
                              setEnhancedImageUrl(null);
                            }}
                            className="text-sm md:text-base"
                          >
                            Remove
                          </Button>
                        </div>
                        {enhancedImageUrl && (
                          <div className="mt-4">
                            <p className="text-sm text-green-600 mb-2">Enhanced Preview:</p>
                            <img 
                              src={enhancedImageUrl} 
                              alt="Enhanced Preview" 
                              className="max-h-48 mx-auto rounded"
                            />
                          </div>
                        )}
                        <p className="text-xs text-gray-500 mt-2">
                          💡 Images will be automatically enhanced when you add the product
                        </p>
                      </div>
                    ) : (
                      <>
                        <Upload className="w-8 h-8 md:w-12 md:h-12 mx-auto mb-4 text-[#205295]" />
                        <p className="text-[#144272] text-sm md:text-base">Click to upload or drag and drop</p>
                        <Input 
                          type="file" 
                          accept="image/*" 
                          className="hidden" 
                          id="imageUpload"
                          onChange={handleImageUpload}
                        />
                        <Button 
                          type="button"
                          variant="outline" 
                          size="sm"
                          className="mt-4 text-sm md:text-base"
                          onClick={() => document.getElementById('imageUpload')?.click()}
                        >
                          Choose File
                        </Button>
                      </>
                    )}
                  </div>
                </div>
                
                <Button 
                  type="submit"
                  className="w-full bg-[#205295] hover:bg-[#144272] text-sm md:text-base"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Adding Product...
                    </>
                  ) : (
                    'Add Product'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  };

  const renderCart = () => (
    <div className="min-h-screen bg-gray-50">
      {renderNavigation()}
      
      <div className="p-4 md:p-6 max-w-4xl mx-auto">
        <h2 className="text-2xl md:text-3xl mb-4 md:mb-6 text-[#0A2647]">Shopping Cart</h2>
        
        {cart.length === 0 ? (
          <Card>
            <CardContent className="p-6 md:p-8 text-center">
              <ShoppingCart className="w-12 h-12 md:w-16 md:h-16 mx-auto mb-4 text-[#205295]" />
              <p className="text-[#144272] text-sm md:text-base">Your cart is empty</p>
              <Link to="/home">
                <Button 
                  className="mt-4 bg-[#205295] hover:bg-[#144272] text-sm md:text-base"
                  size="sm"
                >
                  Continue Shopping
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {cart.map((item) => (
              <Card key={item.id}>
                <CardContent className="p-3 md:p-4 flex flex-col md:flex-row items-start md:items-center space-y-3 md:space-y-0 md:space-x-4">
                  <div className="w-16 h-16 md:w-20 md:h-20 rounded overflow-hidden flex-shrink-0">
                    <ImageWithFallback 
                      src={item.image} 
                      alt={item.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm md:text-lg text-[#0A2647] truncate">{item.name}</h3>
                    <p className="text-[#144272] text-sm md:text-base">${item.price}</p>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                    >
                      <Minus className="w-3 h-3 md:w-4 md:h-4" />
                    </Button>
                    <span className="w-6 md:w-8 text-center text-sm md:text-base">{item.quantity}</span>
                    <Button 
                      size="sm" 
                      variant="outline"
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    >
                      <Plus className="w-3 h-3 md:w-4 md:h-4" />
                    </Button>
                  </div>
                  
                  <div className="text-right">
                    <p className="text-base md:text-lg text-[#205295] font-bold">${item.price * item.quantity}</p>
                    <Button 
                      size="sm" 
                      variant="destructive"
                      onClick={() => removeFromCart(item.id)}
                      className="text-xs md:text-sm"
                    >
                      Remove
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
            
            <Card>
              <CardContent className="p-4">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-lg md:text-xl text-[#0A2647] font-bold">Total: ${getTotalPrice()}</span>
                </div>
                <Button className="w-full bg-[#205295] hover:bg-[#144272] text-sm md:text-base">
                  Proceed to Checkout
                </Button>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );

  const renderAbout = () => (
    <div className="min-h-screen bg-gray-50">
      {renderNavigation()}
      
      <div className="p-4 md:p-6 max-w-4xl mx-auto">
        <div className="text-center mb-8 md:mb-12">
          <img src={varnikaLogo} alt="Varnika" className="h-12 w-12 md:h-16 md:w-16 mx-auto mb-4 md:mb-6" />
          <h2 className="text-2xl md:text-4xl mb-4 md:mb-6 text-[#0A2647]">About Varnika</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 items-center mb-8 md:mb-12">
          <div>
            <h3 className="text-lg md:text-2xl text-[#0A2647] mb-3 md:mb-4">Our Mission</h3>
            <p className="text-[#144272] leading-relaxed mb-4 md:mb-6 text-sm md:text-base">
              Varnika is dedicated to preserving traditional handicrafts and empowering artisans worldwide. 
              We connect talented craftspeople with global markets, ensuring their skills and heritage continue to thrive.
            </p>
            
            <h3 className="text-lg md:text-2xl text-[#0A2647] mb-3 md:mb-4">Our Values</h3>
            <div className="space-y-3 text-sm md:text-base">
              <div>
                <h4 className="font-semibold text-[#0A2647] mb-1">Authenticity</h4>
                <p className="text-[#144272]">Every product on our platform is verified for authenticity, ensuring genuine traditional craftsmanship.</p>
              </div>
              <div>
                <h4 className="font-semibold text-[#0A2647] mb-1">Sustainability</h4>
                <p className="text-[#144272]">We promote eco-friendly practices and sustainable materials in all our handicrafts.</p>
              </div>
              <div>
                <h4 className="font-semibold text-[#0A2647] mb-1">Fair Trade</h4>
                <p className="text-[#144272]">We ensure fair compensation for artisans, supporting their livelihoods and communities.</p>
              </div>
            </div>
          </div>
          
          <div className="space-y-4">
            <div className="rounded-lg overflow-hidden">
              <ImageWithFallback 
                src="https://images.unsplash.com/photo-1716876995651-1ff85b65a6d9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0cmFkaXRpb25hbCUyMGhhbmRpY3JhZnRzJTIwYmFja2dyb3VuZCUyMGFydGlzYW58ZW58MXx8fHwxNzU4MjAzODIwfDA&ixlib=rb-4.1.0&q=80&w=1080" 
                alt="Traditional handicrafts artisan"
                className="w-full h-48 md:h-64 object-cover"
              />
            </div>
          </div>
        </div>

        <div className="mb-8 md:mb-12">
          <h3 className="text-lg md:text-2xl text-[#0A2647] mb-4 text-center">Platform Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
            <div className="bg-white p-4 md:p-6 rounded-lg shadow-sm">
              <h4 className="font-semibold text-[#0A2647] mb-2 text-sm md:text-base">Global Marketplace</h4>
              <p className="text-[#144272] text-sm md:text-base">Connect artisans worldwide with customers who appreciate authentic craftsmanship.</p>
            </div>
            <div className="bg-white p-4 md:p-6 rounded-lg shadow-sm">
              <h4 className="font-semibold text-[#0A2647] mb-2 text-sm md:text-base">Voice-to-Text</h4>
              <p className="text-[#144272] text-sm md:text-base">Easy product descriptions with speech recognition technology.</p>
            </div>
            <div className="bg-white p-4 md:p-6 rounded-lg shadow-sm">
              <h4 className="font-semibold text-[#0A2647] mb-2 text-sm md:text-base">Quality Assurance</h4>
              <p className="text-[#144272] text-sm md:text-base">Rigorous verification process ensures authentic traditional handicrafts.</p>
            </div>
            <div className="bg-white p-4 md:p-6 rounded-lg shadow-sm">
              <h4 className="font-semibold text-[#0A2647] mb-2 text-sm md:text-base">Secure Payments</h4>
              <p className="text-[#144272] text-sm md:text-base">Safe and secure payment processing for all transactions.</p>
            </div>
          </div>
        </div>
        
        <Card className="bg-[#0A2647] text-white">
          <CardContent className="p-6 md:p-8 text-center">
            <h3 className="text-lg md:text-2xl mb-3 md:mb-4">Join the Varnika Community</h3>
            <p className="mb-4 md:mb-6 text-sm md:text-base">
              Whether you're an artisan looking to showcase your work or a buyer seeking authentic handicrafts, 
              Varnika is your gateway to the world of traditional crafts.
            </p>
            <div className="flex flex-col md:flex-row justify-center space-y-3 md:space-y-0 md:space-x-4">
              <Link to="/join">
                <Button 
                  variant="secondary"
                  size="sm"
                  className="text-sm md:text-base"
                >
                  Get Started
                </Button>
              </Link>
              <Link to="/home">
                <Button 
                  variant="outline" 
                  size="sm"
                  className="border-white text-white hover:bg-white hover:text-[#0A2647] text-sm md:text-base"
                >
                  Explore Products
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );

  // Persist state (auth/cart)
  useEffect(() => {
    try {
      const persisted = localStorage.getItem('varnika_state');
      if (persisted) {
        const parsed = JSON.parse(persisted);
        setIsLoggedIn(!!parsed.isLoggedIn);
        setUserType(parsed.userType as UserType);
        setCart(Array.isArray(parsed.cart) ? parsed.cart : []);
      }
    } catch {}
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem('varnika_state', JSON.stringify({ isLoggedIn, userType, cart }));
    } catch {}
  }, [isLoggedIn, userType, cart]);

  return (
    <div className="min-h-screen">
      <Routes>
        <Route path="/" element={renderLandingPage()} />
        <Route path="/join" element={renderUserSelect()} />
        <Route path="/home" element={renderHomePage()} />
        <Route path="/add-product" element={userType === 'seller' ? renderAddProduct() : <Navigate to="/home" replace />} />
        <Route path="/cart" element={userType === 'buyer' ? renderCart() : <Navigate to="/home" replace />} />
        <Route path="/about" element={renderAbout()} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      {renderLoginModal()}
    </div>
  );
};

export default App;