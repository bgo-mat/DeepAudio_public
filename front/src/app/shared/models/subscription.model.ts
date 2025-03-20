export interface Subscription {
    id: number;
    user: number;
    plan: number;
    start_date: string;
    next_payment_date: string;
    stripe_subscription_id: string;
    trial_end: string;
    active: boolean;
}
