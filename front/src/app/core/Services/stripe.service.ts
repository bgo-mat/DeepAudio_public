import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {ApiManagementService} from "./api-management.service";

@Injectable({
  providedIn: 'root'
})
export class StripeService {
  constructor(private apiService: ApiManagementService) { }

  createCheckoutSession(price_id: string): Observable<any> {
    return this.apiService.post(`api/create-checkout-session/`, { price_id });
  }

  retrieveCheckoutSession(sessionId: string): Observable<any> {
    return this.apiService.get(`api/checkout-session/${sessionId}/`);
  }

}
