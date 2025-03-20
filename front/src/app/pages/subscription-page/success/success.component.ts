import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, RouterLink} from "@angular/router";
import {StripeService} from "../../../core/Services/stripe.service";

@Component({
  selector: 'app-success',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './success.component.html',
  styleUrl: './success.component.scss'
})
export class SuccessComponent implements OnInit {
  constructor(private route: ActivatedRoute, public stripeService: StripeService) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const sessionId = params['session_id'];
      if (sessionId) {
        // Optionnel : Vous pouvez récupérer des informations supplémentaires sur la session si nécessaire
        this.stripeService.retrieveCheckoutSession(sessionId).subscribe(response => {
          // Traitez la réponse si nécessaire
          console.log('Checkout Session:', response);
        }, error => {
          console.error('Erreur lors de la récupération de la session de checkout:', error);
        });
      }
    });
  }

}
