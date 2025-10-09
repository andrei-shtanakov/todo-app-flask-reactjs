import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  
  test: {
    // Test Environment
    environment: 'jsdom',
    
    // Global Test APIs (describe, it, expect, etc.)
    globals: true,
    
    // Setup Files
    setupFiles: ['./tests/setup.ts'],
    
    // Coverage Configuration
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json', 'lcov'],
      reportsDirectory: './coverage',
      
      // Coverage Thresholds
      thresholds: {
        statements: 70,
        branches: 60,
        functions: 70,
        lines: 70,
      },
      
      // Files to Include/Exclude
      include: ['src/**/*.{ts,tsx}'],
      exclude: [
        'src/**/*.test.{ts,tsx}',
        'src/**/__tests__/**',
        'src/main.tsx',
        'src/vite-env.d.ts',
        'src/**/*.d.ts',
        '**/node_modules/**',
        '**/dist/**',
      ],
      
      // All flag (include untested files)
      all: true,
    },
    
    // Test Execution
    testTimeout: 10000,
    hookTimeout: 10000,
    
    // Parallel Execution
    threads: true,
    maxThreads: 4,
    minThreads: 1,
    
    // Watch Mode
    watch: false,
    
    // Reporters
    reporters: ['default', 'html', 'json'],
    outputFile: {
      html: './test-results/index.html',
      json: './test-results/results.json',
    },
    
    // Mocking
    mockReset: true,
    restoreMocks: true,
    clearMocks: true,
    
    // CSS/Assets Handling
    css: {
      modules: {
        classNameStrategy: 'non-scoped',
      },
    },
    
    // Include patterns
    include: ['src/**/*.{test,spec}.{ts,tsx}'],
    
    // Exclude patterns
    exclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/cypress/**',
      '**/.{idea,git,cache,output,temp}/**',
      '**/e2e/**',
    ],
  },
  
  // Path Resolution (must match tsconfig paths)
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});

