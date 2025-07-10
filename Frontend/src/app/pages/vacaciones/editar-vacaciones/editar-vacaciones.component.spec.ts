import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditarVacacionesComponent } from './editar-vacaciones.component';

describe('EditarVacacionesComponent', () => {
  let component: EditarVacacionesComponent;
  let fixture: ComponentFixture<EditarVacacionesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditarVacacionesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditarVacacionesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
