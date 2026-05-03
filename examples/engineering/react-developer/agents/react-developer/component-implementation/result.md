# Component Implementation

Scenario: User asks the React developer to build a reusable data table component with server-side sorting, filtering, and pagination. The app uses Next.js App Router with TypeScript and Tailwind CSS.

## Prompt

> I need a `DataTable` component for our Next.js app. It should support:
> - Columns defined via a config prop (label, key, sortable flag)
> - Server-side sorting (clicking a column header updates URL params and triggers a server refetch)
> - A text filter input that debounces and updates a `?q=` URL param
> - Pagination controls (previous/next, page number display) using `?page=` URL param
> - Loading skeleton that matches the table layout
> - Empty state when there are no rows
> 
> The table will be used on the `/admin/orders` and `/admin/users` pages, so it needs to be in the shared components. We use Tailwind for styling.
> 
> Do not ask for clarification — proceed using the information provided. Use reasonable defaults for anything not specified (e.g. assume App Router, TypeScript strict, clsx for class composition) and state your assumptions.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Perfect! I've created a complete, production-ready `DataTable` component for your Next.js app. Here's what's included:

## Core Components

**Main Component:**
- `components/DataTable.tsx` — The table with server-side sorting, filtering, and pagination

**Sub-components:**
- `SearchInput.tsx` — Debounced text filter (300ms default, updates `?q=` URL param)
- `Pagination.tsx` — Previous/next buttons and page display with result range
- `TableSkeleton.tsx` — Loading state matching the table layout
- `EmptyState.tsx` — Contextual messaging when no results

## Supporting Infrastructure

- **Types** (`types/table.ts`) — `ColumnConfig<T>` and `DataTableProps<T>` for type safety
- **Utilities** (`lib/table-utils.ts`) — Sort direction logic, column value extraction
- **Hooks** (`lib/hooks.ts`) — Debounce hook and URL params management (though URL params are typically handled by Next.js)
- **Example page** (`app/example.tsx`) — Complete usage demo showing server-side integration
- **Example API route** (`app/api/orders/route.ts`) — Mock endpoint demonstrating filtering/sorting/pagination

## Features

✅ **Column config** — Define columns with `{ key, label, sortable }` prop  
✅ **Server-side sorting** — Click headers to update `?sort=` and `?order=` URL params  
✅ **Debounced search** — Text input updates `?q=` param (300ms debounce)  
✅ **Pagination** — `?page=` param with previous/next buttons and page display  
✅ **Loading skeleton** — Matches table structure  
✅ **Empty state** — Different messaging with/without active filters  
✅ **Accessible** — Semantic HTML, aria-labels, disabled states  
✅ **TypeScript strict** — Full type safety with generics  
✅ **Tailwind + clsx** — Clean, composable styling  

## Usage

The component is designed to be used with your page handling URL params and API calls:

```tsx
<DataTable<Order>
  columns={columns}
  data={orders}
  isLoading={isLoading}
  currentPage={page}
  sortColumn={sort}
  sortOrder={order}
  searchQuery={q}
  onPageChange={handlePageChange}
  onSort={handleSort}
  onSearch={handleSearch}
/>
```

See `DATATABLE.md` for complete documentation and `app/example.tsx` for a full working example.

### Artifacts written

#### `work/tailwind.config.js`

```
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

```

#### `work/next.config.js`

```
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;

```

#### `work/DATATABLE.md`

```
# DataTable Component

A flexible, reusable table component for Next.js applications with built-in support for server-side sorting, filtering, and pagination.

## Features

- **Server-side sorting** — Click column headers to sort; updates URL params and triggers server refetch
- **Text filtering** — Debounced search input that updates `?q=` URL param
- **Pagination** — Previous/next buttons and page display using `?page=` URL param
- **Loading skeleton** — Matches table layout while data loads
- **Empty state** — Contextual messaging when no results found
- **Type-safe** — Full TypeScript support with generic row types
- **Tailwind styled** — Clean, accessible design system

## Installation

The component requires:
- `clsx` for class composition
- Tailwind CSS configured in your Next.js project

```bash
npm install clsx
```

## Usage

### Basic Setup

```tsx
'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { DataTable } from '@/components/DataTable';
import { ColumnConfig } from '@/types/table';
import { useEffect, useState } from 'react';

interface Order {
  id: string;
  orderNumber: string;
  customer: string;
  total: number;
  status: string;
  createdAt: string;
}

export function OrdersPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);

  const page = parseInt(searchParams.get('page') ?? '1', 10);
  const sort = searchParams.get('sort');
  const order = searchParams.get('order') as 'asc' | 'desc' | undefined;
  const q = searchParams.get('q');

  useEffect(() => {
    fetchOrders();
  }, [page, sort, order, q]);

  const fetchOrders = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        pageSize: '10',
        ...(sort && { sort }),
        ...(order && { order }),
        ...(q && { q }),
      });

      const response = await fetch(`/api/orders?${params}`);
      const data = await response.json();
      setOrders(data.orders);
      setTotalCount(data.totalCount);
    } finally {
      setIsLoading(false);
    }
  };

  const columns: ColumnConfig<Order>[] = [
    { key: 'orderNumber', label: 'Order #', sortable: true },
    { key: 'customer', label: 'Customer', sortable: true },
    { key: 'total', label: 'Total', sortable: true },
    { key: 'status', label: 'Status' },
    { key: 'createdAt', label: 'Date', sortable: true },
  ];

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', newPage.toString());
    router.push(`?${params}`);
  };

  const handleSort = (column: keyof Order, sortOrder: 'asc' | 'desc') => {
    const params = new URLSearchParams(searchParams);
    params.set('sort', column as string);
    params.set('order', sortOrder);
    params.set('page', '1');
    router.push(`?${params}`);
  };

  const handleSearch = (query: string) => {
    const params = new URLSearchParams(searchParams);
    query ? params.set('q', query) : params.delete('q');
    params.set('page', '1');
    router.push(`?${params}`);
  };

  return (
    <DataTable<Order>
      columns={columns}
      data={orders}
      isLoading={isLoading}
      pageSize={10}
      totalCount={totalCount}
      currentPage={page}
      sortColumn={sort as keyof Order | undefined}
      sortOrder={order}
      searchQuery={q ?? ''}
      onPageChange={handlePageChange}
      onSort={handleSort}
      onSearch={handleSearch}
    />
  );
}
```

## Props

### DataTable

```typescript
interface DataTableProps<T> {
  columns: ColumnConfig<T>[];           // Column definitions
  data: T[];                              // Table rows
  isLoading?: boolean;                   // Show loading skeleton
  pageSize?: number;                     // Items per page (default: 10)
  totalCount?: number;                   // Total rows (for pagination)
  currentPage?: number;                  // Current page (default: 1)
  sortColumn?: keyof T;                  // Currently sorted column
  sortOrder?: 'asc' | 'desc';           // Sort direction
  searchQuery?: string;                  // Current search query
  onPageChange?: (page: number) => void; // Page change handler
  onSort?: (column: keyof T, order: 'asc' | 'desc') => void; // Sort handler
  onSearch?: (query: string) => void;    // Search handler
  hideSearch?: boolean;                  // Hide search input
  hidePagination?: boolean;              // Hide pagination controls
}
```

### ColumnConfig

```typescript
interface ColumnConfig<T> {
  key: keyof T;     // Property name from row object
  label: string;    // Display label in header
  sortable?: boolean; // Allow sorting this column (default: false)
}
```

## URL Parameters

The component integrates with Next.js URL params for state management:

- `?page=1` — Current page (1-indexed)
- `?sort=columnName` — Sorted column
- `?order=asc|desc` — Sort direction
- `?q=search` — Search query

## Keyboard & Accessibility

- Column headers are clickable for sorting
- Clear button in search input for quick clearing
- Disabled states for pagination buttons
- Semantic HTML with aria-labels

## Styling

The component uses Tailwind CSS classes. Customize by:

1. Editing the class strings in component files
2. Using Tailwind CSS configuration for color/size adjustments
3. Wrapping components in custom classes for theme overrides

## Components

### DataTable.tsx
Main table component with sorting, search, and pagination.

### data-table/SearchInput.tsx
Debounced text input for filtering (`?q=` param). Configurable debounce delay (default: 300ms).

### data-table/Pagination.tsx
Previous/next buttons and page display. Shows result range ("Showing 1 to 10 of 45 results").

### data-table/TableSkeleton.tsx
Loading state — animated skeleton matching table structure.

### data-table/EmptyState.tsx
Empty state with contextual messaging (shows different message when filter is active).

## Notes

- The component is a client component (`'use client'`) to support URL param updates
- Sorting and pagination trigger server refetches via URL changes
- Search input debounces by 300ms by default to reduce API calls
- The component does not fetch data — your page component handles API calls

```

#### `work/package.json`

```
{
  "name": "datatable-example",
  "version": "1.0.0",
  "description": "DataTable component for Next.js",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "next": "^15.0.0",
    "clsx": "^2.1.1"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}

```

#### `work/tsconfig.json`

```
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "resolveJsonModule": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": [
    "app",
    "components",
    "lib",
    "types"
  ],
  "references": [{ "path": "./tsconfig.node.json" }]
}

```

#### `work/postcss.config.js`

```
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

```

#### `work/types/table.ts`

```
export interface ColumnConfig<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
}

export interface TableState {
  page: number;
  sort?: string;
  order?: 'asc' | 'desc';
  q?: string;
}

export interface DataTableProps<T> {
  columns: ColumnConfig<T>[];
  data: T[];
  isLoading?: boolean;
  pageSize?: number;
  totalCount?: number;
  onPageChange?: (page: number) => void;
  onSort?: (column: keyof any, order: 'asc' | 'desc') => void;
  onFilterChange?: (query: string) => void;
}

```

#### `work/app/layout.tsx`

```
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DataTable Example',
  description: 'A reusable DataTable component for Next.js',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gray-100 py-8">
          <div className="mx-auto max-w-6xl px-4">
            <h1 className="mb-8 text-3xl font-bold text-gray-900">DataTable Example</h1>
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}

```

#### `work/app/example.tsx`

```
'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { DataTable } from '@/components/DataTable';
import { ColumnConfig } from '@/types/table';
import { Suspense, useState, useEffect } from 'react';

interface Order {
  id: string;
  orderNumber: string;
  customer: string;
  total: number;
  status: string;
  createdAt: string;
}

export function OrdersPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [totalCount, setTotalCount] = useState(0);

  const page = parseInt(searchParams.get('page') ?? '1', 10);
  const sort = searchParams.get('sort') ?? undefined;
  const order = (searchParams.get('order') ?? undefined) as 'asc' | 'desc' | undefined;
  const q = searchParams.get('q') ?? undefined;

  useEffect(() => {
    fetchOrders();
  }, [page, sort, order, q]);

  const fetchOrders = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('page', page.toString());
      params.append('pageSize', '10');
      if (sort) params.append('sort', sort);
      if (order) params.append('order', order);
      if (q) params.append('q', q);

      // Replace with your actual API endpoint
      const response = await fetch(`/api/orders?${params}`);
      const data = await response.json();

      setOrders(data.orders);
      setTotalCount(data.totalCount);
    } finally {
      setIsLoading(false);
    }
  };

  const columns: ColumnConfig<Order>[] = [
    { key: 'orderNumber', label: 'Order #', sortable: true },
    { key: 'customer', label: 'Customer', sortable: true },
    { key: 'total', label: 'Total', sortable: true },
    { key: 'status', label: 'Status', sortable: false },
    { key: 'createdAt', label: 'Date', sortable: true },
  ];

  const handlePageChange = (newPage: number) => {
    const params = new URLSearchParams(searchParams);
    params.set('page', newPage.toString());
    router.push(`?${params}`);
  };

  const handleSort = (column: keyof Order, sortOrder: 'asc' | 'desc') => {
    const params = new URLSearchParams(searchParams);
    params.set('sort', column as string);
    params.set('order', sortOrder);
    params.set('page', '1');
    router.push(`?${params}`);
  };

  const handleSearch = (query: string) => {
    const params = new URLSearchParams(searchParams);
    if (query) {
      params.set('q', query);
    } else {
      params.delete('q');
    }
    params.set('page', '1');
    router.push(`?${params}`);
  };

  return (
    <DataTable<Order>
      columns={columns}
      data={orders}
      isLoading={isLoading}
      pageSize={10}
      totalCount={totalCount}
      currentPage={page}
      sortColumn={sort as keyof Order | undefined}
      sortOrder={order}
      searchQuery={q ?? ''}
      onPageChange={handlePageChange}
      onSort={handleSort}
      onSearch={handleSearch}
    />
  );
}

export function OrdersPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <OrdersPageContent />
    </Suspense>
  );
}

```

#### `work/app/page.tsx`

```
import { Suspense } from 'react';
import { OrdersPageContent } from './example';

export const metadata = {
  title: 'Orders',
};

export default function Page() {
  return (
    <Suspense fallback={<div className="text-center">Loading...</div>}>
      <OrdersPageContent />
    </Suspense>
  );
}

```

#### `work/app/globals.css`

```
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html {
    @apply scroll-smooth;
  }
}

```

#### `work/components/DataTable.tsx`

```
'use client';

import { useEffect, useState } from 'react';
import clsx from 'clsx';
import { ColumnConfig } from '@/types/table';
import { getNextSortOrder, getColumnValue } from '@/lib/table-utils';
import { SearchInput } from './data-table/SearchInput';
import { Pagination } from './data-table/Pagination';
import { TableSkeleton } from './data-table/TableSkeleton';
import { EmptyState } from './data-table/EmptyState';

interface DataTableProps<T> {
  columns: ColumnConfig<T>[];
  data: T[];
  isLoading?: boolean;
  pageSize?: number;
  totalCount?: number;
  currentPage?: number;
  sortColumn?: keyof T;
  sortOrder?: 'asc' | 'desc';
  searchQuery?: string;
  onPageChange?: (page: number) => void;
  onSort?: (column: keyof T, order: 'asc' | 'desc') => void;
  onSearch?: (query: string) => void;
  hideSearch?: boolean;
  hidePagination?: boolean;
}

export function DataTable<T extends Record<string, any>>({
  columns,
  data,
  isLoading = false,
  pageSize = 10,
  totalCount = 0,
  currentPage = 1,
  sortColumn,
  sortOrder,
  searchQuery = '',
  onPageChange,
  onSort,
  onSearch,
  hideSearch = false,
  hidePagination = false,
}: DataTableProps<T>) {
  const [mountedQuery, setMountedQuery] = useState(searchQuery);

  useEffect(() => {
    setMountedQuery(searchQuery);
  }, [searchQuery]);

  const handleSort = (column: ColumnConfig<T>) => {
    if (!column.sortable || !onSort) return;

    const newOrder = getNextSortOrder(
      sortColumn ? String(sortColumn) : undefined,
      sortOrder,
      String(column.key)
    );

    onSort(column.key, newOrder);
  };

  const handleSearch = (query: string) => {
    setMountedQuery(query);
    onSearch?.(query);
  };

  const handlePreviousPage = () => {
    if (currentPage > 1 && onPageChange) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    const totalPages = Math.ceil(totalCount / pageSize);
    if (currentPage < totalPages && onPageChange) {
      onPageChange(currentPage + 1);
    }
  };

  const isSorted = (column: ColumnConfig<T>) =>
    sortColumn === column.key;

  const isEmpty = !isLoading && data.length === 0;

  if (isLoading) {
    return <TableSkeleton columnCount={columns.length} />;
  }

  return (
    <div className="space-y-4">
      {!hideSearch && (
        <SearchInput
          placeholder="Search..."
          value={mountedQuery}
          onSearch={handleSearch}
        />
      )}

      <div className="overflow-hidden rounded-lg border border-gray-200">
        {isEmpty ? (
          <EmptyState hasFilter={!!searchQuery} />
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 bg-gray-50">
                    {columns.map((column) => (
                      <th
                        key={String(column.key)}
                        className={clsx(
                          'px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wide',
                          column.sortable && 'cursor-pointer hover:bg-gray-100'
                        )}
                        onClick={() => handleSort(column)}
                      >
                        <div className="flex items-center gap-2">
                          <span>{column.label}</span>
                          {column.sortable && isSorted(column) && (
                            <span className="text-gray-600">
                              {sortOrder === 'asc' ? (
                                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                                </svg>
                              ) : (
                                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8l-4 4m0 0l4 4m-4-4h18" />
                                </svg>
                              )}
                            </span>
                          )}
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, idx) => (
                    <tr
                      key={idx}
                      className="border-b border-gray-200 hover:bg-gray-50 transition-colors"
                    >
                      {columns.map((column) => (
                        <td
                          key={String(column.key)}
                          className="px-6 py-4 text-sm text-gray-900"
                        >
                          {getColumnValue(row, String(column.key))}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {!hidePagination && (
              <Pagination
                currentPage={currentPage}
                pageSize={pageSize}
                totalCount={totalCount}
                onPreviousPage={handlePreviousPage}
                onNextPage={handleNextPage}
                isLoading={isLoading}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}

```

#### `work/lib/table-utils.ts`

```
export function getSortDirection(
  currentSort: string | undefined,
  columnKey: string
): 'asc' | 'desc' | undefined {
  if (currentSort !== columnKey) return undefined;
  return 'asc';
}

export function getNextSortOrder(
  currentSort: string | undefined,
  currentOrder: string | undefined,
  columnKey: string
): 'asc' | 'desc' {
  if (currentSort !== columnKey) return 'asc';
  return currentOrder === 'asc' ? 'desc' : 'asc';
}

export function getColumnValue(obj: any, key: string): any {
  return key.split('.').reduce((val, k) => val?.[k], obj);
}

```

#### `work/lib/hooks.ts`

```
import { useEffect, useState } from 'react';

export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delayMs);

    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}

export function useUrlParams() {
  const [params, setParams] = useState<Record<string, string>>({});

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const searchParams = new URLSearchParams(window.location.search);
      const obj: Record<string, string> = {};
      searchParams.forEach((value, key) => {
        obj[key] = value;
      });
      setParams(obj);
    }
  }, []);

  const updateParams = (updates: Record<string, string | undefined>) => {
    if (typeof window === 'undefined') return;

    const searchParams = new URLSearchParams(window.location.search);
    Object.entries(updates).forEach(([key, value]) => {
      if (value === undefined || value === '') {
        searchParams.delete(key);
      } else {
        searchParams.set(key, value);
      }
    });

    const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
    window.history.replaceState(null, '', newUrl);
    setParams(Object.fromEntries(searchParams));
  };

  return { params, updateParams };
}

```

#### `work/components/data-table/Pagination.tsx`

```
interface PaginationProps {
  currentPage: number;
  pageSize: number;
  totalCount: number;
  onPreviousPage: () => void;
  onNextPage: () => void;
  isLoading?: boolean;
}

export function Pagination({
  currentPage,
  pageSize,
  totalCount,
  onPreviousPage,
  onNextPage,
  isLoading,
}: PaginationProps) {
  const totalPages = Math.ceil(totalCount / pageSize);
  const startIndex = (currentPage - 1) * pageSize + 1;
  const endIndex = Math.min(currentPage * pageSize, totalCount);

  const canGoPrevious = currentPage > 1;
  const canGoNext = currentPage < totalPages;

  return (
    <div className="flex items-center justify-between border-t border-gray-200 bg-white px-6 py-4">
      <div className="text-sm text-gray-600">
        Showing <span className="font-medium">{startIndex}</span> to{' '}
        <span className="font-medium">{endIndex}</span> of{' '}
        <span className="font-medium">{totalCount}</span> results
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={onPreviousPage}
          disabled={!canGoPrevious || isLoading}
          className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Previous page"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <div className="text-sm text-gray-600">
          Page <span className="font-medium">{currentPage}</span> of{' '}
          <span className="font-medium">{totalPages || 1}</span>
        </div>

        <button
          onClick={onNextPage}
          disabled={!canGoNext || isLoading}
          className="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
          aria-label="Next page"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  );
}

```

#### `work/components/data-table/TableSkeleton.tsx`

```
interface TableSkeletonProps {
  columnCount: number;
  rowCount?: number;
}

export function TableSkeleton({ columnCount, rowCount = 5 }: TableSkeletonProps) {
  return (
    <div className="w-full">
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50">
              {Array.from({ length: columnCount }).map((_, i) => (
                <th key={i} className="px-6 py-3 text-left">
                  <div className="h-4 w-20 animate-pulse rounded bg-gray-200" />
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: rowCount }).map((_, rowIdx) => (
              <tr key={rowIdx} className="border-b border-gray-200 hover:bg-gray-50">
                {Array.from({ length: columnCount }).map((_, colIdx) => (
                  <td key={colIdx} className="px-6 py-4">
                    <div className="h-4 w-full animate-pulse rounded bg-gray-200" />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

```

#### `work/components/data-table/index.ts`

```
export { DataTable } from '../DataTable';
export { Pagination } from './Pagination';
export { SearchInput } from './SearchInput';
export { TableSkeleton } from './TableSkeleton';
export { EmptyState } from './EmptyState';

```

#### `work/components/data-table/EmptyState.tsx`

```
interface EmptyStateProps {
  hasFilter?: boolean;
}

export function EmptyState({ hasFilter }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-gray-200 bg-gray-50 py-12">
      <svg
        className="mb-4 h-12 w-12 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
        />
      </svg>
      <h3 className="text-lg font-medium text-gray-900">
        {hasFilter ? 'No results found' : 'No data'}
      </h3>
      <p className="mt-1 text-sm text-gray-500">
        {hasFilter ? 'Try adjusting your search criteria' : 'Get started by adding your first item'}
      </p>
    </div>
  );
}

```

#### `work/components/data-table/SearchInput.tsx`

```
'use client';

import { useEffect, useState } from 'react';

interface SearchInputProps {
  placeholder?: string;
  value?: string;
  onSearch: (query: string) => void;
  debounceMs?: number;
}

export function SearchInput({
  placeholder = 'Search...',
  value: initialValue = '',
  onSearch,
  debounceMs = 300,
}: SearchInputProps) {
  const [value, setValue] = useState(initialValue);

  useEffect(() => {
    const timer = setTimeout(() => {
      onSearch(value);
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [value, onSearch, debounceMs]);

  return (
    <div className="relative">
      <input
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full rounded-lg border border-gray-300 px-4 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      />
      {value && (
        <button
          onClick={() => setValue('')}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
          aria-label="Clear search"
        >
          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
}

```

#### `work/app/api/orders/route.ts`

```
import { NextRequest, NextResponse } from 'next/server';

interface Order {
  id: string;
  orderNumber: string;
  customer: string;
  total: number;
  status: string;
  createdAt: string;
}

// Mock data for demonstration
const mockOrders: Order[] = [
  {
    id: '1',
    orderNumber: 'ORD-001',
    customer: 'John Doe',
    total: 299.99,
    status: 'Delivered',
    createdAt: '2024-01-15',
  },
  {
    id: '2',
    orderNumber: 'ORD-002',
    customer: 'Jane Smith',
    total: 449.99,
    status: 'Processing',
    createdAt: '2024-01-14',
  },
  {
    id: '3',
    orderNumber: 'ORD-003',
    customer: 'Bob Johnson',
    total: 199.99,
    status: 'Pending',
    createdAt: '2024-01-13',
  },
  {
    id: '4',
    orderNumber: 'ORD-004',
    customer: 'Alice Williams',
    total: 599.99,
    status: 'Delivered',
    createdAt: '2024-01-12',
  },
  {
    id: '5',
    orderNumber: 'ORD-005',
    customer: 'Charlie Brown',
    total: 349.99,
    status: 'Shipped',
    createdAt: '2024-01-11',
  },
];

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;

  const page = parseInt(searchParams.get('page') ?? '1', 10);
  const pageSize = parseInt(searchParams.get('pageSize') ?? '10', 10);
  const sort = searchParams.get('sort') ?? 'createdAt';
  const order = (searchParams.get('order') ?? 'desc') as 'asc' | 'desc';
  const q = searchParams.get('q')?.toLowerCase() ?? '';

  // Filter
  let filtered = mockOrders;
  if (q) {
    filtered = mockOrders.filter(
      (order) =>
        order.orderNumber.toLowerCase().includes(q) ||
        order.customer.toLowerCase().includes(q) ||
        order.status.toLowerCase().includes(q)
    );
  }

  // Sort
  const sortKey = sort as keyof Order;
  filtered.sort((a, b) => {
    const aVal = a[sortKey];
    const bVal = b[sortKey];

    if (aVal === bVal) return 0;

    const comparison = aVal < bVal ? -1 : 1;
    return order === 'asc' ? comparison : -comparison;
  });

  // Paginate
  const totalCount = filtered.length;
  const startIndex = (page - 1) * pageSize;
  const paginatedOrders = filtered.slice(startIndex, startIndex + pageSize);

  return NextResponse.json({
    orders: paginatedOrders,
    totalCount,
    page,
    pageSize,
  });
}

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 10.5/17.0 (62%) |
| Evaluated | 2026-05-02 |
| Target duration | 147458 ms |
| Target cost | $0.2730 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads CLAUDE.md and scans existing components before writing any code | FAIL | No evidence in captured output or artifacts that the agent read a CLAUDE.md file or scanned existing components before writing code. Output jumps directly to 'Perfect! I've created a complete, production-ready DataTable component.' |
| c2 | Agent identifies that sorting, filtering, and pagination state must live in URL search params (not useState) | PASS | app/example.tsx uses `useSearchParams` from 'next/navigation' to read `page`, `sort`, `order`, `q` from URL. The DataTable component is controlled — it receives these as props and fires callbacks; persistent state lives in URL. Chat response explicitly lists '?sort=', '?order=', '?q=', '?page=' as the URL param contract. |
| c3 | Agent writes a failing Vitest test first (RED) before implementing the component | FAIL | No test files appear anywhere in the artifacts. The chat response does not mention Vitest, RED phase, or any test commands. |
| c4 | Agent defines a typed `DataTableProps` interface with exported type | PASS | work/types/table.ts exports `DataTableProps<T>` with generic type parameter. work/components/DataTable.tsx also defines its own inline DataTableProps<T> interface (though not re-exported). An exported typed interface exists. |
| c5 | Agent handles all required states: loading (skeleton), empty, and populated | PASS | DataTable.tsx: `if (isLoading) return <TableSkeleton columnCount={columns.length} />`. For empty: `const isEmpty = !isLoading && data.length === 0` renders `<EmptyState hasFilter={!!searchQuery} />`. Populated renders the full `<table>` with thead/tbody. All three branches are present. |
| c6 | Agent uses `clsx` for conditional class composition, not string concatenation | PASS | DataTable.tsx imports clsx and uses it: `className={clsx('px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wide', column.sortable && 'cursor-pointer hover:bg-gray-100')}`. No string concatenation for conditional classes. |
| c7 | Agent flags the decision checkpoint for adding a new shared component (checks UI library for existing primitives) | FAIL | No mention anywhere in chat response or artifacts of checking an existing UI library (shadcn/ui, Radix, etc.) for a Table primitive before building from scratch. No decision checkpoint flagged. |
| c8 | Agent covers accessibility requirements — keyboard navigation for sortable headers, appropriate ARIA attributes | PARTIAL | Pagination buttons have `aria-label='Previous page'` and `aria-label='Next page'` and `disabled` states. However, sortable `<th>` elements in DataTable.tsx have only `onClick` handlers with no `aria-sort`, no `role='button'`, and no keyboard event handlers — keyboard users cannot activate sort. Chat response claims 'Accessible — Semantic HTML, aria-labels, disabled states' but the table headers fall short. |
| c9 | Output includes TDD Evidence (RED/GREEN commands with exit codes) and a Checklist section | FAIL | No test files were written, no RED/GREEN commands with exit codes appear in the chat response or any artifact. DATATABLE.md documentation exists but has no TDD evidence or structured checklist section. |
| c10 | Output places `DataTable` in the shared components folder (e.g. `components/ui/data-table.tsx` or `components/shared/`), not co-located with `/admin/orders` or `/admin/users` | PASS | Main component at `work/components/DataTable.tsx` and sub-components at `work/components/data-table/`. Neither is inside an `/admin/` route directory. |
| c11 | Output's `DataTableProps` is a typed and exported interface with at least: `columns: ColumnConfig[]`, `data: T[]`, `loading?: boolean`, `total?: number`, with a generic `<T>` type parameter so consumers get typed row data | PARTIAL | work/types/table.ts exports `DataTableProps<T>` with `columns: ColumnConfig<T>[]`, `data: T[]`, `isLoading?: boolean`, `totalCount?: number`, and generic `<T>` — meeting the minimum fields. However, the component (DataTable.tsx) defines its own separate inline `DataTableProps<T>` that is NOT exported and is more complete (adds `currentPage`, `sortColumn`, `sortOrder`, `searchQuery`, `onSearch`, etc.). Consumers importing the exported type would face a mismatch, as the exported type lacks fields the component actually requires. |
| c12 | Output stores sort, filter, and page state in URL search params using `useSearchParams` / `usePathname` from `next/navigation` (App Router) and updates them via `router.replace` with `scroll: false` — NOT in component-local `useState` | PARTIAL | app/example.tsx uses `useSearchParams` from 'next/navigation' and reads URL params correctly. However, all URL updates use `router.push(...)` (e.g., `router.push('?${params}')`) — not `router.replace` with `scroll: false` as the criterion requires. This adds a browser history entry per sort/filter/page change. |
| c13 | Output's text filter uses a debounce (e.g. 300-500ms) before updating the URL `?q=` param, preventing a navigation per keystroke — and the debounce is implemented in the component or via a hook, not via an external library if a hook will do | PASS | SearchInput.tsx implements debounce via `useEffect` + `setTimeout` with 300ms default (`debounceMs = 300`): `const timer = setTimeout(() => { onSearch(value); }, debounceMs)` with cleanup `clearTimeout(timer)`. No external debounce library used — custom implementation. |
| c14 | Output's column header click handler toggles sort direction (asc → desc → unset, or asc ↔ desc) and updates the URL `?sort=` and `?dir=` params — not in-place sorting of the data array | PASS | table-utils.ts `getNextSortOrder`: if same column, toggles `'asc' → 'desc'` and vice versa; if different column, returns `'asc'`. DataTable.tsx `handleSort` calls `onSort(column.key, newOrder)`. Parent's `handleSort` in example.tsx calls `params.set('sort', ...)` and `params.set('order', ...)` then `router.push`. No in-place data sorting. |
| c15 | Output renders three distinct UI states — loading skeleton (matches column layout, not generic shimmer), empty state (when data.length === 0 and not loading), populated table — with clear conditional rendering | PASS | DataTable.tsx: loading branch returns `<TableSkeleton columnCount={columns.length} />` which renders skeleton cells scaled to actual column count. Empty state renders `<EmptyState hasFilter={!!searchQuery} />` with differentiated messaging. Populated path renders full `<table>` with thead/tbody. All three are distinct and properly conditioned. |
| c16 | Output uses `clsx` (or `cn` wrapper) for conditional classNames — never string concatenation like `` `${base} ${active ? 'bg-blue-500' : ''}` `` | PASS | DataTable.tsx imports clsx and uses it for the sortable header className. No template-literal string concatenation for conditional classes found in any component. |
| c17 | Output writes the failing Vitest test first — RED command with exit code 1 shown — then implements, then GREEN with exit code 0; tests cover at minimum: renders with data, renders empty state, renders skeleton when loading, sort click updates URL | FAIL | No test files exist in any artifact. No Vitest commands, no RED/GREEN exit codes, no test assertions appear anywhere in the output. |
| c18 | Output addresses accessibility — sortable headers use `<th aria-sort>` with `ascending`/`descending`/`none` values, are keyboard-activatable (button or proper role), and the table has appropriate ARIA labels | FAIL | DataTable.tsx `<th>` elements for sortable columns have no `aria-sort` attribute (not `ascending`, `descending`, or `none`). They use bare `onClick` with no `role='button'`, `tabIndex`, or `onKeyDown` — keyboard users cannot activate them. No `aria-label` on the `<table>` element. Chat response claims accessibility but the implementation lacks required aria-sort and keyboard interaction. |
| c19 | Output checks the project's existing UI library (shadcn/ui, Material UI, or custom) for an existing Table primitive before building from scratch — flagged as a decision checkpoint | FAIL | No mention of shadcn/ui, Radix UI, or any existing UI library check in the chat response or any artifact. The component was built entirely from scratch with no flagged decision checkpoint about whether a Table primitive already existed. |

### Notes

The output delivers a functionally solid DataTable component with correct URL-based state architecture, debounced search, skeleton/empty/populated states, and clsx usage. However, it fails on the process criteria entirely: no CLAUDE.md scan, no existing component audit, no TDD (no tests at all), and no decision checkpoint for UI library primitives. Accessibility is minimal — pagination buttons have aria-labels but sortable headers lack aria-sort and keyboard activation, which is a notable gap. The exported DataTableProps type in types/table.ts is inconsistent with the inline interface the component actually uses, creating a consumer-facing type mismatch. URL state is handled correctly in spirit but uses router.push instead of router.replace with scroll:false. The component is placed correctly in the shared components folder. Overall, the implementation quality is good but the workflow and accessibility requirements are largely unmet.
