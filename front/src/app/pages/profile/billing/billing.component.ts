import { Component } from '@angular/core';
import {UserProfileService} from "../user-profil/user-profile.service";

@Component({
  selector: 'app-billing',
  standalone: true,
  imports: [],
  templateUrl: './billing.component.html',
  styleUrl: './billing.component.scss'
})
export class BillingComponent {

constructor(private profilService: UserProfileService) {
}
  billingSession(){
    this.profilService.createBillingSession().subscribe(
        (response :any ) => {
          if (response.url) {
            window.location.href = response.url;
          } else {
            console.error("URL du portail non reçue.");
          }
        },
        (error: any) => {
          console.error("Erreur lors de la création de la session de facturation :", error);
        }
    );
  }

  deleteSub(){
    this.profilService.deleteSubService().subscribe(
        (response :any ) => {
          console.log(response)
        },
        (error: any) => {
          console.error("Erreur lors de la création de la session de facturation :", error);
        }
    );
  }
}
