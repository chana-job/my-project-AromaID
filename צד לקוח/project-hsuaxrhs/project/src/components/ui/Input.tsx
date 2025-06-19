import React, { forwardRef } from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  id: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, id, className = '', ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={id}
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={id}
          className={`
            w-full rounded-md border border-gray-300 px-3 py-2 text-sm
            placeholder-gray-400 shadow-sm focus:border-blue-500 focus:outline-none
            focus:ring-1 focus:ring-blue-500 disabled:cursor-not-allowed
            disabled:bg-gray-50 disabled:text-gray-500
            ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''}
            ${className}
          `}
          {...props}
        />
        {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;