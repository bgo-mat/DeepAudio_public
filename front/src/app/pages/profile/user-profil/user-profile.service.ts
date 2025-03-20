import { Injectable } from '@angular/core';
import {ApiManagementService} from "../../../core/Services/api-management.service";
import {Observable} from "rxjs";
import { Subscription } from '../../../shared/models/subscription.model';


@Injectable({
  providedIn: 'root'
})
export class UserProfileService {

  constructor(private apiManagement: ApiManagementService) { }

  test(){
    return this.apiManagement.get("api/transaction/");
  }
  test2(){
    return this.apiManagement.get("api/subscription/");
  }

  createBillingSession(){
    return this.apiManagement.post("api/stripe-portal-session/");
  }

  deleteSubService(){
    return this.apiManagement.post("api/cancel-subscription/");
  }

  getfavoriteCall(){
    return this.apiManagement.get(`api/favorites/`);
  }

  getCurrentSubscription(): Observable<Subscription[]> {
    return this.apiManagement.get<Subscription[]>('api/subscription/');
  }
}
