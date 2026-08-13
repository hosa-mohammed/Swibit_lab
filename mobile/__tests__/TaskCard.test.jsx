import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import TaskCard from '../components/TaskCard';

describe('TaskCard', () => {
  const mockTask = {
    id: 1,
    title: 'Test Task',
    description: 'Test Description',
    priority: 'high',
    is_complete: false,
  };

  it('renders task information correctly', () => {
    const { getByText } = render(
      <TaskCard task={mockTask} onPress={() => {}} onDelete={() => {}} />
    );

    expect(getByText('Test Task')).toBeTruthy();
    expect(getByText('Test Description')).toBeTruthy();
    expect(getByText('high')).toBeTruthy();
  });

  it('calls onPress when card is pressed', () => {
    const onPressMock = jest.fn();
    const { getByText } = render(
      <TaskCard task={mockTask} onPress={onPressMock} onDelete={() => {}} />
    );

    fireEvent.press(getByText('Test Task'));
    expect(onPressMock).toHaveBeenCalled();
  });

  it('calls onDelete when delete button is pressed', () => {
    const onDeleteMock = jest.fn();
    const { getByText } = render(
      <TaskCard task={mockTask} onPress={() => {}} onDelete={onDeleteMock} />
    );

    fireEvent.press(getByText('Delete'));
    expect(onDeleteMock).toHaveBeenCalled();
  });

  it('shows completed task with strikethrough', () => {
    const completedTask = { ...mockTask, is_complete: true };
    const { getByText } = render(
      <TaskCard task={completedTask} onPress={() => {}} onDelete={() => {}} />
    );

    const titleText = getByText('Test Task');
    expect(titleText.props.style).toMatchObject(
      expect.objectContaining({ textDecorationLine: 'line-through' })
    );
  });
});