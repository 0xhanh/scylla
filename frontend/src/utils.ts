// import * as process from 'process'

// export function getBaseURL(): string {
//     return process.env['NODE_ENV'] === 'production' ? prodURL() : 'http://localhost:8899';
// }

export function getBaseURL(): string {
    // Check if we're in development mode by looking at the URL
    // This works in both development and production environments
    if (window.location.hostname === 'localhost' && (window.location.port === '5173' || window.location.port === '8899')) {
        return 'http://localhost:8899';
    }
    return prodURL();
}

function prodURL(): string {
    const location = window.location;
    return location.protocol + "//" + location.host;
}

export interface Proxy {
    id: number;
    ip: string;
    port: number;
    is_valid: boolean;
    created_at: number;
    updated_at: number;
    latency: number;
    stability: number;
    is_anonymous: boolean;
    is_https: boolean;
    location: string;
    organization: string;
    region: string;
    country: string;
    city: string;
}

export interface ResponseJSON {
    proxies: Proxy[];
    count: number;
    per_page: number;
    page: number;
    total_page: number;
}

export interface StatsResponseJSON {
    mean: number;
    median: number;
    total_count: number;
    valid_count: number;
}