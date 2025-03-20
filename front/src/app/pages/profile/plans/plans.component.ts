import {Component, OnInit} from '@angular/core';
import {UserProfileService} from "../user-profil/user-profile.service";
import {data} from "autoprefixer";
import { Subscription } from '../../../shared/models/subscription.model';
import {DatePipe, NgIf} from "@angular/common";

@Component({
  selector: 'app-plans',
  standalone: true,
  imports: [
    DatePipe,
    NgIf
  ],
  templateUrl: './plans.component.html',
  styleUrl: './plans.component.scss'
})
export class PlansComponent implements OnInit{

  constructor(private profileService: UserProfileService) {}

  loading = true;
  subscription: Subscription | null = null;

  ngOnInit(): void {
    this.fetchSubscription();
  }

  fetchSubscription(): void {
    this.profileService.getCurrentSubscription().subscribe(
        (data: Subscription[]) => {
          this.subscription = data[0];
          console.log(this.subscription)
          this.loading = false;
        },
        (error) => {
          console.error('Erreur lors de la récupération de l’abonnement :', error);
          this.loading = false;
        }
    );
  }
}
