'use client';

export default function Simple3DBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 animate-pulse"></div>
      
      {/* Floating 3D elements */}
      <div className="absolute inset-0">
        {/* Large floating orbs */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full blur-xl opacity-20 animate-float-3d"
            style={{
              width: `${Math.random() * 200 + 100}px`,
              height: `${Math.random() * 200 + 100}px`,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              background: [
                'linear-gradient(45deg, #3b82f6, #8b5cf6)',
                'linear-gradient(45deg, #ec4899, #f59e0b)',
                'linear-gradient(45deg, #10b981, #3b82f6)',
                'linear-gradient(45deg, #8b5cf6, #ec4899)'
              ][i % 4],
              animationDelay: `${i * 0.5}s`,
              animationDuration: `${8 + i * 2}s`
            }}
          />
        ))}
        
        {/* Geometric shapes */}
        {[...Array(12)].map((_, i) => (
          <div
            key={`geo-${i}`}
            className="absolute opacity-10 animate-spin-3d"
            style={{
              width: `${Math.random() * 60 + 20}px`,
              height: `${Math.random() * 60 + 20}px`,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              background: `linear-gradient(45deg, ${
                ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b'][i % 4]
              }, transparent)`,
              borderRadius: i % 2 === 0 ? '50%' : '0%',
              transform: `rotate(${i * 30}deg)`,
              animationDelay: `${i * 0.3}s`,
              animationDuration: `${15 + i}s`
            }}
          />
        ))}
      </div>
      
      {/* CSS Variables for animations */}
      <style jsx>{`
        @keyframes float-3d {
          0%, 100% {
            transform: translateY(0px) translateX(0px) rotateY(0deg) scale(1);
          }
          25% {
            transform: translateY(-30px) translateX(20px) rotateY(90deg) scale(1.1);
          }
          50% {
            transform: translateY(-10px) translateX(-20px) rotateY(180deg) scale(0.9);
          }
          75% {
            transform: translateY(20px) translateX(10px) rotateY(270deg) scale(1.05);
          }
        }
        
        @keyframes spin-3d {
          0% {
            transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
          }
          33% {
            transform: rotateX(120deg) rotateY(120deg) rotateZ(120deg);
          }
          66% {
            transform: rotateX(240deg) rotateY(240deg) rotateZ(240deg);
          }
          100% {
            transform: rotateX(360deg) rotateY(360deg) rotateZ(360deg);
          }
        }
        
        .animate-float-3d {
          animation: float-3d ease-in-out infinite;
        }
        
        .animate-spin-3d {
          animation: spin-3d linear infinite;
        }
      `}</style>
    </div>
  );
}