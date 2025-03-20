import { Injectable } from '@angular/core';
import {Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class PopupService {

  private popupVisibility = new Subject<boolean>();
  popupVisibility$ = this.popupVisibility.asObservable();

  private noCreditsPopupVisibility = new Subject<boolean>();
  noCreditsPopupVisibility$ = this.noCreditsPopupVisibility.asObservable();

  showPopup() {
    this.popupVisibility.next(true);
  }

  hidePopup() {
    this.popupVisibility.next(false);
  }

  showNoCreditsPopup() {
    this.noCreditsPopupVisibility.next(true);
  }

  hideNoCreditsPopup() {
    this.noCreditsPopupVisibility.next(false);
  }
}
