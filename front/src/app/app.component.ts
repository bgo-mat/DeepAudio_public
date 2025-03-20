import {Component, OnInit} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {AuthService} from "./core/Services/auth/auth.service";
import {ToggleThemeComponent} from "./shared/components/toggle-theme/toggle-theme.component";
import {NavBarComponent} from "./shared/components/nav-bar/nav-bar.component";
import {AuthPopupComponent} from "./shared/components/auth-popup/auth-popup.component";
import {CreditPopupComponent} from "./shared/components/credit-popup/credit-popup.component";

@Component({
  selector: 'app-root',
  standalone: true,
    imports: [RouterOutlet, ToggleThemeComponent, NavBarComponent, AuthPopupComponent, CreditPopupComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit{
  title = 'deep-audio';

  constructor(private authService: AuthService) {}

  ngOnInit() {
    this.authService.initializeUserStatus();
  }
}
