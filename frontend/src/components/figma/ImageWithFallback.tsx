import React, { useState } from 'react'

const ERROR_IMG_SRC =
  'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODgiIGhlaWdodD0iODgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBvcGFjaXR5PSIuMyIgZmlsbD0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIzLjciPjxyZWN0IHg9IjE2IiB5PSIxNiIgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiByeD0iNiIvPjxwYXRoIGQ9Im0xNiA1OCAxNi0xOCAzMiAzMiIvPjxjaXJjbGUgY3g9IjUzIiBjeT0iMzUiIHI9IjciLz48L3N2Zz4KCg=='

const LOADING_IMG_SRC =
  'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iODgiIGhlaWdodD0iODgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2Utd2lkdGg9IjMiPjxjaXJjbGUgY3g9IjQ0IiBjeT0iNDQiIHI9IjIwIiBzdHJva2UtZGFzaGFycmF5PSIzMS40MTYiIHN0cm9rZS1kYXNob2Zmc2V0PSIzMS40MTYiPjxhbmltYXRlVHJhbnNmb3JtIGF0dHJpYnV0ZU5hbWU9InRyYW5zZm9ybSIgYXR0cmlidXRlVHlwZT0ieG1sIiB0eXBlPSJyb3RhdGUiIGR1cj0iMnMiIHJlcGVhdENvdW50PSJpbmRlZmluaXRlIiB2YWx1ZXM9IjAgNDQgNDQ7MzYwIDQ0IDQ0Ii8+PC9jaXJjbGU+PC9zdmc+'

export function ImageWithFallback(props: React.ImgHTMLAttributes<HTMLImageElement>) {
  const [didError, setDidError] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  const handleError = () => {
    setDidError(true)
    setIsLoading(false)
  }

  const handleLoad = () => {
    setIsLoading(false)
  }

  const { src, alt, style, className, ...rest } = props

  // Handle empty or invalid src
  if (!src || src.trim() === '') {
    return (
      <div
        className={`inline-block bg-gray-100 text-center align-middle ${className ?? ''}`}
        style={style}
      >
        <div className="flex items-center justify-center w-full h-full">
          <div className="text-gray-400 text-sm">No Image</div>
        </div>
      </div>
    )
  }

  return didError ? (
    <div
      className={`inline-block bg-gray-100 text-center align-middle ${className ?? ''}`}
      style={style}
    >
      <div className="flex items-center justify-center w-full h-full">
        <div className="text-center">
          <img src={ERROR_IMG_SRC} alt="Error loading image" className="w-8 h-8 mx-auto mb-2 opacity-50" />
          <div className="text-gray-500 text-xs">Image not available</div>
        </div>
      </div>
    </div>
  ) : (
    <div className="relative">
      {isLoading && (
        <div
          className={`absolute inset-0 flex items-center justify-center bg-gray-100 ${className ?? ''}`}
          style={style}
        >
          <img src={LOADING_IMG_SRC} alt="Loading..." className="w-8 h-8 animate-spin" />
        </div>
      )}
      <img 
        src={src} 
        alt={alt} 
        className={`${className} ${isLoading ? 'opacity-0' : 'opacity-100'} transition-opacity duration-300`} 
        style={style} 
        {...rest} 
        onError={handleError}
        onLoad={handleLoad}
      />
    </div>
  )
}
