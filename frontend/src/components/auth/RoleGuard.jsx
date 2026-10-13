import React from 'react';
import { Navigate } from 'react-router-dom';

export function RoleGuard({ children, allowedRoles }) {
    const role = localStorage.getItem('user_role'); // In a real app, use Zustand/Context
    const isAuthenticated = !!localStorage.getItem('access_token');

    if (!isAuthenticated) return <Navigate to="/login" replace />;
    if (allowedRoles && !allowedRoles.includes(role)) return <Navigate to="/unauthorized" replace />;

    return children;
}
