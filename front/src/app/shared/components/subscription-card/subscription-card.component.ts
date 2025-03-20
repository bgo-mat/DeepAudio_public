// subscription-card.component.ts
import {Component, Input, Output, EventEmitter} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";

@Component({
  selector: 'app-subscription-card',
  templateUrl: './subscription-card.component.html',
  standalone: true,
  imports: [
    NgForOf,
    NgIf
  ],
  styleUrls: ['./subscription-card.component.scss']
})
export class SubscriptionCardComponent {
  @Input() title: string = '';
  @Input() price: number = 0;
  @Input() monthlyPrice: number = 0;
  @Input() description: string = '';
  @Input() features: string[] = [];
  @Input() period: 'monthly' | 'annually' = 'monthly';
  @Output() subscribe = new EventEmitter<void>();

  get annualOriginalPrice(): string {
    return (this.monthlyPrice * 12).toFixed(2);
  }

  get annualDiscountedPrice(): string {
    return this.price.toFixed(2);
  }

  onSubscribe() {
    this.subscribe.emit();
  }
}
