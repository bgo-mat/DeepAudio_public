import {Component, OnDestroy, OnInit} from '@angular/core';
import {Subscription} from "rxjs";
import {PopupService} from "../auth-popup/auth-popup.service";
import {Router} from "@angular/router";
import { trigger, style, transition, animate } from '@angular/animations';
import {NgIf} from "@angular/common";
import {AuthService} from "../../../core/Services/auth/auth.service";

@Component({
  selector: 'app-credit-popup',
  standalone: true,
  imports: [
    NgIf
  ],
  templateUrl: './credit-popup.component.html',
  styleUrl: './credit-popup.component.scss',
  animations: [
    trigger('popupAnimation', [
      transition(':enter', [
        style({ transform: 'scale(0.9)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'scale(1)', opacity: 1 })),
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ transform: 'scale(0.9)', opacity: 0 })),
      ]),
    ]),
  ],
})
export class CreditPopupComponent implements OnInit, OnDestroy{
  isVisible = false;
  private subscription: Subscription;
  creditStatus:number = 0;

  constructor(private popupService: PopupService, private router: Router, private authService: AuthService) {
    this.subscription = this.popupService.noCreditsPopupVisibility$.subscribe(
        (visible) => {
          this.isVisible = visible;
        }
    );
  }

  ngOnInit() {
    this.authService.getUserStatus().subscribe(status => {
      this.creditStatus = status.tokens;
    });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  close() {
    this.popupService.hideNoCreditsPopup();
  }

  goToStore() {
    this.router.navigate(['/subscription']);
    this.popupService.hideNoCreditsPopup();
  }
}
