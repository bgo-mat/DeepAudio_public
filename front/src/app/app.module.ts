import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HTTP_INTERCEPTORS, HttpClientModule } from "@angular/common/http";
import { RequestInterceptor } from "./core/Services/request-interceptor.service";
import { BrowserModule } from "@angular/platform-browser";
import { RouterModule } from '@angular/router';
import { routes } from "./app.routes";
import { NgxStripeModule } from 'ngx-stripe';
import {environment} from "../environments/environment";


@NgModule({
  declarations: [],
  imports: [
    RouterModule.forRoot(routes),
    CommonModule,
    BrowserModule,
    HttpClientModule,
    NgxStripeModule.forRoot(environment.stripePublicKey),
  ],
  exports: [RouterModule],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: RequestInterceptor,
      multi: true
    }
  ],
})
export class AppModule {}
