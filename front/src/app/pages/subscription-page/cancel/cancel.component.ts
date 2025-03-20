import {Component, OnInit} from '@angular/core';
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-cancel',
  standalone: true,
  imports: [
    RouterLink
  ],
  templateUrl: './cancel.component.html',
  styleUrl: './cancel.component.scss'
})
export class CancelComponent implements OnInit {
  constructor() { }

  ngOnInit(): void { }
}
