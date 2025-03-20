import { Component } from '@angular/core';
import {NgClass, NgForOf} from "@angular/common";
import {SubscriptionCardComponent} from "../../shared/components/subscription-card/subscription-card.component";
import {NavBarComponent} from "../../shared/components/nav-bar/nav-bar.component";
import { loadStripe, Stripe } from '@stripe/stripe-js';
import {StripeService} from "../../core/Services/stripe.service";
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-subscription-page',
  templateUrl: './subscription-page.component.html',
  standalone: true,
  imports: [
    NgClass,
    SubscriptionCardComponent,
    NgForOf,
    NavBarComponent
  ],
  styleUrls: ['./subscription-page.component.scss']
})
export class SubscriptionPageComponent {
  selectedPeriod: 'monthly' | 'annually' = 'monthly';

  constructor(private stripeService : StripeService) {
  }

  monthlySubscriptions = [
    {
      title: 'LITE',
      price: 4.99,
      monthlyPrice: 4.99, // Ajoute cette ligne
      description: 'Best option for personal use & for your next project.',
      features: [
        'Individual configuration',
        'No setup, or hidden fees',
        'Team size: 1 developer',
        'Premium support: 6 months',
        'Free updates: 6 months'
      ],
      stripePriceId: 'price_1QJJexAmpv2h0RJtqpwqetaV'
    },
    {
      title: 'PLUS',
      price: 9.99,
      monthlyPrice: 9.99, // Ajoute cette ligne
      description: 'Ideal for growing businesses that want more customers.',
      features: [
        'Priority configuration',
        'No hidden fees',
        'Team size: Up to 10 developers',
        'Premium support: 12 months',
        'Free updates: 12 months'
      ],
      stripePriceId: 'price_1QF0tVAmpv2h0RJt6L1dun0x'
    },
    {
      title: 'PREMIUM',
      price: 14.99,
      monthlyPrice: 14.99, // Ajoute cette ligne
      description: 'Best for large businesses that need advanced solutions.',
      features: [
        'Custom configuration',
        'Dedicated support team',
        'Unlimited team size',
        'Premium support: 24 months',
        'Free updates: Lifetime'
      ],
      stripePriceId: 'price_1QF0vkAmpv2h0RJtwRZPC2PJ'
    }
  ];

  annuallySubscriptions = [
    {
      title: 'LITE',
      price: 49.99, // Prix annuel réduit
      monthlyPrice: 4.99, // Prix mensuel pour le calcul du prix barré
      description: 'Best option for personal use & for your next project.',
      features: [
        'Individual configuration',
        'No setup, or hidden fees',
        'Team size: 1 developer',
        'Premium support: 6 months',
        'Free updates: 6 months'
      ],
      stripePriceId: 'price_1QF0rEAmpv2h0RJtLTusXlG9'
    },
    {
      title: 'PLUS',
      price: 99.99,
      monthlyPrice: 9.99,
      description: 'Ideal for growing businesses that want more customers.',
      features: [
        'Priority configuration',
        'No hidden fees',
        'Team size: Up to 10 developers',
        'Premium support: 12 months',
        'Free updates: 12 months'
      ],
      stripePriceId: 'price_1QF0uiAmpv2h0RJt7thrXdG2'
    },
    {
      title: 'PREMIUM',
      price: 149.99,
      monthlyPrice: 14.99,
      description: 'Best for large businesses that need advanced solutions.',
      features: [
        'Custom configuration',
        'Dedicated support team',
        'Unlimited team size',
        'Premium support: 24 months',
        'Free updates: Lifetime'
      ],
      stripePriceId: 'price_1QF0wxAmpv2h0RJtV0KOh4Z7'
    }
  ];

  selectPeriod(period: 'monthly' | 'annually') {
    this.selectedPeriod = period;
  }

  async subscribe(subscription: any) {
    console.log(subscription)
    try {
      const session = await this.stripeService.createCheckoutSession(subscription.stripePriceId).toPromise();
      const stripe = await loadStripe(environment.stripePublicKey);
      if (stripe) {
        await stripe.redirectToCheckout({ sessionId: session.sessionId });
      } else {
        console.error('Stripe.js failed to load.');
      }
    } catch (error: any) {
      console.error('Error creating checkout session:', error);
    }
  }
}
