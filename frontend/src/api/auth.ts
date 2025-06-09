import apiClient from './client';

export interface LoginCredentials {
  username: string;
  password: string;
  remember_me?: boolean;
}

export interface SignupData {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
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
  };
}

export interface RefreshTokenResponse {
  access: string;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
  confirm_password: string;
}

export const authAPI = {
  // Login
  login: (credentials: LoginCredentials) =>
    apiClient.post<LoginResponse>('/auth/login/', credentials),

  // Signup
  signup: (data: SignupData) =>
    apiClient.post('/auth/users/', data),

  // Refresh token
  refreshToken: (refreshToken: string) =>
    apiClient.post<RefreshTokenResponse>('/auth/refresh/', {
      refresh: refreshToken,
    }),

  // Get current user
  getCurrentUser: () =>
    apiClient.get('/auth/users/me/'),

  // Update user profile
  updateProfile: (data: any) =>
    apiClient.patch('/auth/users/update_profile/', data),

  // Change password
  changePassword: (data: ChangePasswordData) =>
    apiClient.post('/auth/users/change_password/', data),

  // Get user statistics (admin only)
  getUserStats: () =>
    apiClient.get('/auth/users/stats/'),

  // Get user sessions
  getUserSessions: () =>
    apiClient.get('/auth/sessions/current_user_sessions/'),

  // Terminate session
  terminateSession: (sessionId: number) =>
    apiClient.post(`/auth/sessions/${sessionId}/terminate/`),

  // Get activity logs
  getActivityLogs: () =>
    apiClient.get('/auth/activities/my_activities/'),

  // Log dashboard view
  logDashboardView: () =>
    apiClient.post('/auth/dashboard/log_view/'),

  // Get dashboard overview
  getDashboardOverview: () =>
    apiClient.get('/auth/dashboard/overview/'),

  // Get recent activities
  getRecentActivities: () =>
    apiClient.get('/auth/dashboard/recent_activities/'),

  // Get districts
  getDistricts: () =>
    apiClient.get('/auth/districts/'),

  // Get sectors
  getSectors: (districtId?: number) =>
    apiClient.get('/auth/sectors/', {
      params: districtId ? { district: districtId } : undefined,
    }),
};