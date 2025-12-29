import React, { createContext, useState, useContext, ReactNode, useEffect, useCallback } from 'react';

// Define the shape of user metadata
interface UserMetadata {
    softwareBackground?: 'Beginner' | 'Intermediate' | 'Advanced';
    hardwareBackground?: 'None' | 'Basic' | 'Advanced';
    // Add other metadata fields as needed
}

// Define the shape of the user object
interface User {
    id: string;
    email: string;
    name?: string; // For OAuth users
    photoUrl?: string; // For OAuth users
    metadata?: UserMetadata;
}

// Define the shape of the context data
interface AuthContextType {
    user: User | null;
    token: string | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<boolean>;
    signup: (email: string, password: string, metadata: UserMetadata) => Promise<boolean>;
    oauthLogin: (provider: 'google' | 'github') => Promise<boolean>;
    logout: () => void;
    updateUserMetadata: (metadata: UserMetadata) => Promise<boolean>;
}

// Create the context with a default undefined value
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Helper for simulating API calls
const simulateApiCall = (success: boolean, delay: number = 1000) => {
    return new Promise<boolean>((resolve, reject) => {
        setTimeout(() => {
            if (success) {
                resolve(true);
            } else {
                reject(new Error('Simulated API call failed'));
            }
        }, delay);
    });
};

// Create a provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [token, setToken] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);

    // Simulate session restoration
    useEffect(() => {
        const storedUser = localStorage.getItem('mock_user');
        const storedToken = localStorage.getItem('mock_token');
        if (storedUser && storedToken) {
            setUser(JSON.parse(storedUser));
            setToken(storedToken);
        }
        setLoading(false);
    }, []);

    const saveSession = useCallback((loggedInUser: User, sessionToken: string) => {
        setUser(loggedInUser);
        setToken(sessionToken);
        localStorage.setItem('mock_user', JSON.stringify(loggedInUser));
        localStorage.setItem('mock_token', sessionToken);
    }, []);

    const clearSession = useCallback(() => {
        setUser(null);
        setToken(null);
        localStorage.removeItem('mock_user');
        localStorage.removeItem('mock_token');
    }, []);

    const login = useCallback(async (email: string, password: string) => {
        setLoading(true);
        try {
            // Simulate API call to Better Auth login endpoint
            await simulateApiCall(true); // Always succeed for mock

            const mockUser: User = { id: 'mock-id-' + email, email: email, name: email.split('@')[0] };
            const mockToken = `mock-jwt-for-${email}`;
            saveSession(mockUser, mockToken);
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            return false;
        } finally {
            setLoading(false);
        }
    }, [saveSession]);

    const signup = useCallback(async (email: string, password: string, metadata: UserMetadata) => {
        setLoading(true);
        try {
            // Simulate API call to Better Auth signup endpoint
            await simulateApiCall(true); // Always succeed for mock

            const mockUser: User = { id: 'mock-id-' + email, email: email, name: email.split('@')[0], metadata: metadata };
            const mockToken = `mock-jwt-for-${email}`;
            saveSession(mockUser, mockToken);
            return true;
        } catch (error) {
            console.error('Signup failed:', error);
            return false;
        } finally {
            setLoading(false);
        }
    }, [saveSession]);

    const oauthLogin = useCallback(async (provider: 'google' | 'github') => {
        setLoading(true);
        try {
            // Simulate redirect to OAuth provider and callback
            await simulateApiCall(true); // Always succeed for mock

            const mockUser: User = { 
                id: `mock-oauth-id-${provider}`, 
                email: `${provider}-user@example.com`,
                name: `${provider} User`,
                photoUrl: `https://via.placeholder.com/150/${provider}.png` // Mock photo
            };
            const mockToken = `mock-jwt-for-${provider}`;
            saveSession(mockUser, mockToken);
            return true;
        } catch (error) {
            console.error('OAuth login failed:', error);
            return false;
        } finally {
            setLoading(false);
        }
    }, [saveSession]);

    const logout = useCallback(() => {
        clearSession();
        window.location.href = '/'; // Redirect to home page after logout
    }, [clearSession]);

    const updateUserMetadata = useCallback(async (newMetadata: UserMetadata) => {
        if (!user) return false;
        setLoading(true);
        try {
            await simulateApiCall(true); // Always succeed for mock
            const updatedUser: User = { ...user, metadata: { ...(user.metadata || {}), ...newMetadata } };
            saveSession(updatedUser, token || ''); // Resave with updated user
            return true;
        } catch (error) {
            console.error('Failed to update metadata:', error);
            return false;
        } finally {
            setLoading(false);
        }
    }, [user, token, saveSession]);


    const contextValue = {
        user,
        token,
        loading,
        login,
        signup,
        oauthLogin,
        logout,
        updateUserMetadata,
    };

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};

// Create a custom hook to use the auth context
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
