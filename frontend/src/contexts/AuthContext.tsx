import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authAPI } from '../api/auth';

// Types
export interface User {
  id: number;
  username: string;
  full_name: string;
  role: string;
  role_verbose: string;
  district: string | null;
  permissions: {
    can_view_agriculture: boolean;
    can_view_health: boolean;
    can_view_education: boolean;
    can_manage_users: boolean;
    can_generate_reports: boolean;
    can_manage_alerts: boolean;
    can_export_data: boolean;
  };
  preferred_language: string;
}

export interface AuthState {
  user: User | null;
  tokens: {
    access: string | null;
    refresh: string | null;
  };
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: { user: User; tokens: { access: string; refresh: string } } }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'CLEAR_ERROR' };

// Initial state
const initialState: AuthState = {
  user: null,
  tokens: {
    access: localStorage.getItem('access_token'),
    refresh: localStorage.getItem('refresh_token'),
  },
  isAuthenticated: false,
  isLoading: true,
  error: null,
};

// Reducer
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        tokens: action.payload.tokens,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        tokens: { access: null, refresh: null },
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        tokens: { access: null, refresh: null },
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

// Context
interface AuthContextType extends AuthState {
  login: (username: string, password: string, rememberMe?: boolean) => Promise<void>;
  logout: () => void;
  updateUser: (user: User) => void;
  clearError: () => void;
}

// Export the context so it can be imported
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      const accessToken = localStorage.getItem('access_token');
      const refreshToken = localStorage.getItem('refresh_token');

      if (accessToken && refreshToken) {
        try {
          // Verify token and get user info
          const userResponse = await authAPI.getCurrentUser();
          dispatch({
            type: 'AUTH_SUCCESS',
            payload: {
              user: userResponse.data,
              tokens: { access: accessToken, refresh: refreshToken },
            },
          });
        } catch (error) {
          // Token might be expired, try to refresh
          try {
            const refreshResponse = await authAPI.refreshToken(refreshToken);
            const newAccessToken = refreshResponse.data.access;
            
            localStorage.setItem('access_token', newAccessToken);
            
            // Get user info with new token
            const userResponse = await authAPI.getCurrentUser();
            dispatch({
              type: 'AUTH_SUCCESS',
              payload: {
                user: userResponse.data,
                tokens: { access: newAccessToken, refresh: refreshToken },
              },
            });
          } catch (refreshError) {
            // Refresh failed, clear tokens
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            dispatch({ type: 'LOGOUT' });
          }
        }
      } else {
        dispatch({ type: 'LOGOUT' });
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string, rememberMe = false): Promise<void> => {
    dispatch({ type: 'AUTH_START' });

    try {
      const requestData = { 
        username, 
        password, 
        remember_me: rememberMe 
      };
      
      console.log('Attempting login with:', { 
        ...requestData, 
        password: '***' 
      });
      
      // Log the actual request being made
      console.log('Request URL:', `${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/auth/login/`);
      console.log('Request headers:', {
        'Content-Type': 'application/json',
      });
      
      const response = await authAPI.login(requestData);
      console.log('Login response:', response);
      
      const { access, refresh, user } = response.data;

      // Store tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      dispatch({
        type: 'AUTH_SUCCESS',
        payload: {
          user,
          tokens: { access, refresh },
        },
      });
    } catch (error: any) {
      console.error('Login error:', error);
      console.error('Error response:', error.response);
      console.error('Error response data:', error.response?.data);
      console.error('Error response status:', error.response?.status);
      console.error('Error response headers:', error.response?.headers);
      
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message || 
                          error.response?.data?.error ||
                          error.response?.data?.non_field_errors?.[0] ||
                          'Login failed. Please check your credentials.';
      
      dispatch({
        type: 'AUTH_FAILURE',
        payload: errorMessage,
      });
    }
  };

  const logout = (): void => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    dispatch({ type: 'LOGOUT' });
  };

  const updateUser = (user: User): void => {
    dispatch({ type: 'UPDATE_USER', payload: user });
  };

  const clearError = (): void => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: AuthContextType = {
    ...state,
    login,
    logout,
    updateUser,
    clearError,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};