import {Component, EventEmitter, Output} from '@angular/core';
import {Router} from "@angular/router";
import {PopupService} from "./auth-popup.service";
import {Subscription} from "rxjs";
import {NgIf} from "@angular/common";
import {animate, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'app-auth-popup',
  standalone: true,
    imports: [
        NgIf
    ],
  templateUrl: './auth-popup.component.html',
  styleUrl: './auth-popup.component.scss',
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
export class AuthPopupComponent {
  isVisible = false;
  private subscription: Subscription;

  constructor(private popupService: PopupService, private router: Router) {
    this.subscription = this.popupService.popupVisibility$.subscribe(
        (visible) => {
          this.isVisible = visible;
        }
    );
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  close() {
    this.popupService.hidePopup();
  }

  signIn() {
    this.router.navigate(['/connexion']);
    this.popupService.hidePopup();
  }

  signUp() {
    this.router.navigate(['/register']);
    this.popupService.hidePopup();
  }
}
