import 'package:flutter/material.dart';
import '../services/api_service.dart';

class HealthTab extends StatefulWidget {
  final ApiService apiService;
  
  const HealthTab({super.key, required this.apiService});

  @override
  State<HealthTab> createState() => _HealthTabState();
}

class _HealthTabState extends State<HealthTab> {
  List<dynamic> _records = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadRecords();
  }

  Future<void> _loadRecords() async {
    try {
      final records = await widget.apiService.getHealthRecords();
      setState(() {
        _records = records;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _addRecord() async {
    final typeController = TextEditingController();
    final valueController = TextEditingController();
    final unitController = TextEditingController();
    
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Add Health Record'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: typeController,
              decoration: const InputDecoration(labelText: 'Type (e.g., weight, exercise)'),
            ),
            TextField(
              controller: valueController,
              decoration: const InputDecoration(labelText: 'Value'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: unitController,
              decoration: const InputDecoration(labelText: 'Unit (e.g., kg, minutes)'),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Add'),
          ),
        ],
      ),
    );

    if (result == true && typeController.text.isNotEmpty) {
      try {
        await widget.apiService.createHealthRecord({
          'record_type': typeController.text,
          'value': valueController.text.isNotEmpty ? double.tryParse(valueController.text) : null,
          'unit': unitController.text.isEmpty ? null : unitController.text,
        });
        _loadRecords();
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error creating record: $e')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _records.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.favorite_outline, size: 64, color: Colors.grey),
                      const SizedBox(height: 16),
                      const Text('No health records yet'),
                      const SizedBox(height: 8),
                      ElevatedButton(
                        onPressed: _addRecord,
                        child: const Text('Add Your First Record'),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _records.length,
                  itemBuilder: (context, index) {
                    final record = _records[index];
                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        leading: const Icon(Icons.favorite, color: Colors.red),
                        title: Text(record['record_type'] ?? ''),
                        subtitle: Text(
                          record['value'] != null
                              ? '${record['value']} ${record['unit'] ?? ''}'
                              : record['notes'] ?? '',
                        ),
                        trailing: Text(
                          record['recorded_at'] != null
                              ? record['recorded_at'].toString().substring(0, 10)
                              : '',
                        ),
                      ),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addRecord,
        child: const Icon(Icons.add),
      ),
    );
  }
}

