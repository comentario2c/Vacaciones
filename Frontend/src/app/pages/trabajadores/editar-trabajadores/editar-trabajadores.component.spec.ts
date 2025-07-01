import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditarTrabajadoresComponent } from './editar-trabajadores.component';

describe('EditarTrabajadoresComponent', () => {
  let component: EditarTrabajadoresComponent;
  let fixture: ComponentFixture<EditarTrabajadoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditarTrabajadoresComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditarTrabajadoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
