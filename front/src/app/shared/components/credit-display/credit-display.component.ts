import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../../core/Services/auth/auth.service";
import {NgIf} from "@angular/common";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-credit-display',
  standalone: true,
  imports: [
    NgIf,
    RouterLink
  ],
  templateUrl: './credit-display.component.html',
  styleUrl: './credit-display.component.scss'
})
export class CreditDisplayComponent implements OnInit{

  constructor(private authService: AuthService) {}

  userStatus: string | null = '';
  creditStatus: number = 0;

  ngOnInit() {
    this.authService.getUserStatus().subscribe(status => {
      this.userStatus = status.role;
      this.creditStatus = status.tokens;
    })
  }

}
