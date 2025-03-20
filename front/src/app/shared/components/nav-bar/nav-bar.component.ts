// nav-bar.component.ts
import { Component, OnInit } from '@angular/core';
import { ButtonActionComponent } from "../buttons/button-action/button-action.component";
import { NgClass, NgIf } from "@angular/common";
import { RouterLink } from '@angular/router';
import { CreditDisplayComponent } from "../credit-display/credit-display.component";
import { AuthService } from "../../../core/Services/auth/auth.service";
import {ToggleThemeComponent} from "../toggle-theme/toggle-theme.component";
import {SearchBarComponent} from "../search-bar/search-bar.component";

@Component({
  selector: 'app-nav-bar',
  standalone: true,
    imports: [
        ButtonActionComponent,
        NgClass,
        NgIf,
        RouterLink,
        CreditDisplayComponent,
        ToggleThemeComponent,
        SearchBarComponent
    ],
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit {

  isMenuOpen = false;
  isConnect: boolean = false;
  isVisitor: boolean = false;

  constructor(private authService: AuthService) {}

  ngOnInit() {

    this.authService.getUserStatus().subscribe(status => {
      this.isConnect = status.isConnected;
      this.isVisitor = (status.role === 'VISITOR');
    });
  }

  public handleLogOut() {
    this.authService.logOut().subscribe(() => {
      this.isConnect = false;
    });
  }
  public toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }
}
