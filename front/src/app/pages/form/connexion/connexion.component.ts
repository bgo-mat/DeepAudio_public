import { Component } from '@angular/core';
import {Router, RouterLink} from '@angular/router';
import { AuthService } from '../../../core/Services/auth/auth.service';
import {NgIf} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NavBarComponent} from "../../../shared/components/nav-bar/nav-bar.component";

@Component({
  selector: 'app-connexion',
  standalone: true,
  templateUrl: './connexion.component.html',
  imports: [
    RouterLink,
    NgIf,
    FormsModule,
    NavBarComponent
  ],
  styleUrls: ['./connexion.component.scss']
})
export class ConnexionComponent {
  email: string = '';
  password: string = '';
  rememberMe: boolean = false;
  errorMessage: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  public login(): void {
    this.authService.logIn(this.email, this.password, this.rememberMe).subscribe({
      next: () => {
        this.router.navigate(['/']);
      },
      error: (error) => {
        console.error('Erreur lors de la connexion :', error);
        this.errorMessage = 'Invalid credentials';
      }
    });
  }
}
