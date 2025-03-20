import {Component, OnInit} from '@angular/core';
import {NavBarComponent} from "../../../shared/components/nav-bar/nav-bar.component";
import {RouterLink} from '@angular/router';
import { AuthService } from '../../../core/Services/auth/auth.service';
import { Router } from '@angular/router';
import {FormsModule} from "@angular/forms";
import {NgIf} from "@angular/common";
import {CategoryService} from "../../../core/Services/music/category/category.service";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  standalone: true,
  imports: [
    RouterLink,
    FormsModule,
    NavBarComponent,
    NgIf
  ],
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit{
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  errorMessage: string = '';
  accept_newsletter: boolean = true;

  constructor(private authService: AuthService, private router: Router, private categoryService: CategoryService) {}

  ngOnInit() {
    this.categoryService.getAllCategory().subscribe(
        data => {
          console.log(data)
        }
    )
  }

  onSubmit() {
    if (this.password !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match';
      return;
    }

    this.authService.signIn(this.email, this.password, this.accept_newsletter).subscribe({
      next: () => {
        this.router.navigate(['/connexion']);
      },
      error: (error) => {
        console.error('Erreur lors de l\'inscription :', error);
        this.errorMessage = 'An error occurred during registration';
      }
    });
  }
}
